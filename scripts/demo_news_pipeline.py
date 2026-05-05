#!/usr/bin/env python3
"""
DEMO: 4-Layer News Pipeline (Inspired by Aksara Baru AI)
Run: python3 scripts/demo_news_pipeline.py
"""
import json, sys, os
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def layer1_collect():
    """L1: Collect data from IDX"""
    log("=" * 50)
    log("LAYER 1: DATA COLLECTION")
    log("=" * 50)
    
    log("Fetching IDX disclosures...")
    from curl_cffi import requests
    
    url = 'https://www.idx.co.id/primary/NewsAnnouncement/GetAllAnnouncement'
    params = {'pageSize': 50, 'pageNumber': 1, 'kodeEmiten': ''}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.idx.co.id/',
        'Origin': 'https://www.idx.co.id',
    }
    resp = requests.get(url, params=params, headers=headers, impersonate='chrome', timeout=30)
    items = resp.json().get('Items', [])
    
    log(f"✅ Collected {len(items)} disclosures")
    return items

def layer2_draft(data):
    """L2: Generate draft (simulasi — karena butuh LLM)"""
    log("\n" + "=" * 50)
    log("LAYER 2: DRAFT GENERATION")
    log("=" * 50)
    
    # Filter for news-worthy items
    keywords = ['dividen', 'buyback', 'obligasi', 'laba', 'siaran pers',
                'volatilitas', 'penjualan saham', 'akuisisi']
    
    candidates = []
    for item in data:
        title = item.get('Title', '')
        if any(kw in title.lower() for kw in keywords):
            candidates.append(item)
    
    log(f"Found {len(candidates)} news-worthy items")
    
    drafts = []
    for item in candidates[:3]:
        code = item.get('Code', '').strip()
        title = item.get('Title', '')
        publish = item.get('PublishDate', '')
        
        draft = {
            "code": code,
            "title": title,
            "publish": publish,
            "draft_ready": True
        }
        drafts.append(draft)
        log(f"  ✅ [{code}] {title[:60]}...")
    
    return drafts

def layer3_quality(drafts):
    """L3: Quality Gate"""
    log("\n" + "=" * 50)
    log("LAYER 3: QUALITY GATE")
    log("=" * 50)
    
    passed = []
    for draft in drafts:
        checks = {
            "has_title": len(draft.get('title', '')) > 10,
            "has_code": bool(draft.get('code')),
            "has_date": bool(draft.get('publish')),
            "has_content": draft.get('draft_ready', False)
        }
        
        all_passed = all(checks.values())
        score = sum(1 for v in checks.values() if v) / len(checks) * 100
        
        log(f"  [{draft['code']}] Score: {score:.0f}% | Passed: {'✅' if all_passed else '❌'}")
        
        if all_passed:
            passed.append(draft)
    
    return passed

def layer4_polish(drafts):
    """L4: Polish & Output"""
    log("\n" + "=" * 50)
    log("LAYER 4: POLISH & OUTPUT")
    log("=" * 50)
    
    for draft in drafts:
        log(f"\n📰 [{draft['code']}] {draft['title']}")
        log(f"   Published: {draft['publish']}")
        log(f"   Status: ✅ READY — Dapat dipoles lebih lanjut dengan LLM")
        log(f"   Tone options: CNBC Indonesia, Kontan, Bisnis.com")
    
    return drafts

def main():
    log("🚀 AUTO NEWS PIPELINE — DEMO")
    log(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Run 4 layers
    data = layer1_collect()
    drafts = layer2_draft(data)
    
    if not drafts:
        log("\n❌ No news-worthy items found today")
        return
    
    passed = layer3_quality(drafts)
    articles = layer4_polish(passed)
    
    log("\n" + "=" * 50)
    log(f"✅ PIPELINE COMPLETE: {len(articles)} articles ready")
    log("=" * 50)
    log("\n📋 NEXT STEPS:")
    log("   1. Polish dengan advanced LLM (Tone: CNBC/Kontan)")
    log("   2. Quality Gate final check")
    log("   3. Tambah disclaimer")
    log("   4. Publish ke WordPress / output ke user")

if __name__ == "__main__":
    main()
