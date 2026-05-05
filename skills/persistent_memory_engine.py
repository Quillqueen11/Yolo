#!/usr/bin/env python3
"""
persistent_memory engine — Long-term memory with Chroma vector DB.
Layers: L1 working, L2 episodic, L3 semantic, L4 procedural.
"""
import os, sys, json, time, re
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path(__file__).parent.parent.parent
DATA_DIR = BASE / 'data' / 'persistent_memory'
DATA_DIR.mkdir(parents=True, exist_ok=True)

CHROMA_DIR = DATA_DIR / 'chroma'
COLLECTION_NAME = 'persistent_memory'

# Lazy-loaded Chroma
_chroma = None
_collection = None

def log(msg):
    print(f'[MEMORY] {msg}')

def get_chroma():
    global _chroma, _collection
    if _chroma is None:
        import chromadb
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
        try:
            _collection = _chroma.get_collection(COLLECTION_NAME)
        except:
            _collection = _chroma.create_collection(COLLECTION_NAME)
    return _collection

_embedder = None
def get_embedder():
    """Get embedding function (cached)."""
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer('all-MiniLM-L6-v2')
    return _embedder

# ═══════════════════════════════════════════
# CORE: STORE
# ═══════════════════════════════════════════

def store(content, tags=None, layer="episodic", importance=0.5, source="", metadata=None):
    """Store a memory in vector DB."""
    collection = get_chroma()
    embedder = get_embedder()
    
    memory_id = f'mem_{datetime.now().strftime("%Y%m%d%H%M%S")}_{hash(content) % 10000:04d}'
    
    tags_str = ','.join(tags) if tags else ''
    ts = datetime.now().isoformat()
    
    meta = {
        'timestamp': ts,
        'layer': layer,
        'importance': importance,
        'tags': tags_str,
        'source': source,
        'content_len': len(content),
    }
    if metadata:
        meta.update(metadata)
    
    # Check if semantically similar memory already exists
    existing = recall(content, n_results=1, min_score=0.95)
    if existing:
        score = existing[0]['score']
        log(f'⏭ Similar memory exists (score: {score:.2f}), skipping')
        return existing[0]['id']
    
    # Embed and store
    embedding = embedder.encode(content).tolist()
    
    collection.add(
        ids=[memory_id],
        embeddings=[embedding],
        documents=[content],
        metadatas=[meta]
    )
    
    log(f'✅ Stored: {memory_id} ({layer}, importance={importance})')
    log(f'   Content: {content[:80]}...')
    return memory_id

# ═══════════════════════════════════════════
# CORE: RECALL
# ═══════════════════════════════════════════

def recall(query, n_results=5, min_score=0.3, layer=None, tags=None):
    """Retrieve related memories by semantic similarity."""
    collection = get_chroma()
    embedder = get_embedder()
    
    query_embedding = embedder.encode(query).tolist()
    
    where = {}
    if layer:
        where['layer'] = layer
    if tags:
        # Chroma $contains doesn't work well, filter post-query
        pass
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results * 3,  # Get more, filter by score
        where=where if where else None
    )
    
    if not results['ids'] or not results['ids'][0]:
        return []
    
    memories = []
    for i in range(len(results['ids'][0])):
        mem = {
            'id': results['ids'][0][i],
            'content': results['documents'][0][i],
            'metadata': results['metadatas'][0][i],
            'score': 1.0 - results['distances'][0][i] if results['distances'][0][i] <= 1.0 else 0.0
        }
        if mem['score'] >= min_score:
            memories.append(mem)
    
    # Sort by importance * score
    memories.sort(key=lambda m: m['metadata'].get('importance', 0.5) * m['score'], reverse=True)
    
    return memories[:n_results]

# ═══════════════════════════════════════════
# CORE: LEARN (pattern extraction)
# ═══════════════════════════════════════════

def learn(trigger, lesson, action=""):
    """Store a learned pattern in semantic memory layer."""
    return store(
        content=f"PATTERN: {trigger} → {lesson}. Action: {action}",
        tags=['pattern', 'learned'],
        layer='semantic',
        importance=0.9,
        source='self_learn',
        metadata={'trigger': trigger, 'lesson': lesson, 'action': action}
    )

def detect_patterns():
    """Analyze episodic memories and extract patterns."""
    collection = get_chroma()
    
    # Get all memories
    all_mem = collection.get()
    if not all_mem['ids']:
        return []
    
    patterns = []
    
    # Count by hour pattern (e.g., IDX timeout at 05:00)
    hour_counts = {}
    for i, meta in enumerate(all_mem['metadatas']):
        if 'timestamp' in meta and 'timeout' in all_mem['documents'][i].lower():
            try:
                hour = meta['timestamp'].split('T')[1].split(':')[0]
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
            except:
                pass
    
    for hour, count in hour_counts.items():
        if count >= 2:
            pattern_content = f"PATTERN: Multiple timeouts detected at hour {hour}"
            patterns.append({
                'pattern': f'Timeout at hour {hour}',
                'confidence': count / max(hour_counts.values()),
                'count': count
            })
    
    return patterns

# ═══════════════════════════════════════════
# CORE: FORGET (prune)
# ═══════════════════════════════════════════

def forget(older_than_days=30, importance_below=0.3, dry_run=True):
    """Delete old/unimportant memories."""
    collection = get_chroma()
    
    all_mem = collection.get()
    if not all_mem['ids']:
        log('No memories to forget')
        return 0
    
    cutoff = datetime.now() - timedelta(days=older_than_days)
    to_delete = []
    
    for i, mem_id in enumerate(all_mem['ids']):
        meta = all_mem['metadatas'][i]
        
        # Check age
        old = False
        if 'timestamp' in meta:
            try:
                ts = datetime.fromisoformat(meta['timestamp'])
                if ts < cutoff:
                    old = True
            except:
                pass
        
        # Check importance
        unimportant = meta.get('importance', 0.5) < importance_below
        
        if old and unimportant:
            to_delete.append(mem_id)
    
    if dry_run:
        log(f'Would delete {len(to_delete)} old/unimportant memories (dry run)')
        return len(to_delete)
    
    if to_delete:
        collection.delete(ids=to_delete)
        log(f'Deleted {len(to_delete)} old/unimportant memories')
    
    return len(to_delete)

# ═══════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════

def summary():
    """Show memory stats."""
    collection = get_chroma()
    all_mem = collection.get()
    
    if not all_mem['ids']:
        print('No memories stored yet.')
        return
    
    total = len(all_mem['ids'])
    layers = {}
    importances = []
    
    for meta in all_mem['metadatas']:
        l = meta.get('layer', 'unknown')
        layers[l] = layers.get(l, 0) + 1
        importances.append(meta.get('importance', 0.5))
    
    avg_imp = sum(importances) / len(importances) if importances else 0
    
    print(f'📊 MEMORY SUMMARY')
    print(f'   Total: {total} memories')
    print(f'   Layers:')
    for l, c in sorted(layers.items()):
        print(f'     - {l}: {c}')
    print(f'   Avg importance: {avg_imp:.2f}')
    
    # Recent
    recent = sorted(all_mem['metadatas'], key=lambda m: m.get('timestamp', ''), reverse=True)[:3]
    print(f'   Recent:')
    for r in recent:
        print(f'     - {r.get("timestamp","?")[:16]} [{r.get("layer","?")}] imp={r.get("importance",0.5)}')

# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Persistent memory engine')
    parser.add_argument('action', choices=['store', 'recall', 'learn', 'forget', 'summary', 'detect'])
    parser.add_argument('content', nargs='?', default=None)
    parser.add_argument('--tags', default='', help='Comma-separated tags')
    parser.add_argument('--layer', default='episodic', choices=['working', 'episodic', 'semantic', 'procedural'])
    parser.add_argument('--importance', type=float, default=0.5)
    parser.add_argument('--source', default='cli')
    parser.add_argument('--n', type=int, default=5, help='Number of results')
    parser.add_argument('--min-score', type=float, default=0.3)
    parser.add_argument('--older-than', type=int, default=30, help='Days')
    parser.add_argument('--importance-below', type=float, default=0.3)
    parser.add_argument('--trigger', default='')
    parser.add_argument('--lesson', default='')
    parser.add_argument('--dry-run', action='store_true')
    
    args = parser.parse_args()
    
    if args.action == 'store':
        if not args.content:
            print('❌ content required')
            sys.exit(1)
        store(args.content, tags=args.tags.split(',') if args.tags else None,
              layer=args.layer, importance=args.importance, source=args.source)
    
    elif args.action == 'recall':
        if not args.content:
            print('❌ query required')
            sys.exit(1)
        results = recall(args.content, n_results=args.n, min_score=args.min_score)
        print(f'Found {len(results)} memories:')
        for r in results:
            print(f'  [{r["score"]:.2f}] ({r["metadata"].get("layer","?")}) {r["content"][:100]}')
    
    elif args.action == 'learn':
        if not args.trigger or not args.lesson:
            print('❌ --trigger and --lesson required')
            sys.exit(1)
        learn(args.trigger, args.lesson)
    
    elif args.action == 'forget':
        forget(older_than_days=args.older_than, importance_below=args.importance_below, dry_run=args.dry_run)
    
    elif args.action == 'summary':
        summary()
    
    elif args.action == 'detect':
        patterns = detect_patterns()
        print(f'Found {len(patterns)} patterns:')
        for p in patterns:
            print(f'  [{p["confidence"]:.0%}] {p["pattern"]} (x{p["count"]})')
