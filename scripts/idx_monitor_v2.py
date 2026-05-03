#!/usr/bin/env python3
"""
IDX Corporate Action Monitor v2
- Fetches via curl_cffi (no browser)
- Enriches with Tavily web search
- Stores in Chroma vector DB (sentence-transformers)
- Sends to Telegram
"""

import os
import json
import time
from datetime import datetime

import chromadb
from curl_cffi import requests
from tavily import TavilyClient
from sentence_transformers import SentenceTransformer

# PDF reader skill
import sys
sys.path.insert(0, str(__file__).rsplit("/", 1)[0] + "/..")
from skills.pdf_reader.pdf_reader import fetch_pdf_text, extract_key_info

# ─── Config ──────────────────────────────────────────────────────────────────
BASE_URL = "https://www.idx.co.id"
CHROMA_PATH = "/app/working/workspaces/default/data/chroma_db"
STATE_FILE = "/app/working/workspaces/default/data/idx_action_state.json"
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = "924535843"
TAVILY_KEY = "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"
EMBED_MODEL = "all-MiniLM-L6-v2"
PDF_MAX_PAGES = 3  # Limit pages for speed

# ─── Filter ───────────────────────────────────────────────────────────────────
EXCLUDE = [
    "laporan kepemilikan", "perubahan kepemilikan saham",
    "laporan tahunan", "keberlanjutan", "esg",
    "rencana penyampaian laporan keuangan",
    "pemanggilan rapat", "pemanggilan rups", "pemberitahuan rups",
    "undangan rapat", "undangan rups",
    "bukti iklan", "rumus penyesuaian", "penyesuaian waran",
    "rencana laporan keuangan",
]

INCLUDE = [
    "direksi", "dewan komisaris",
    "penawaran umum", "stock split", "reverse stock", "delisting",
    "buyback", "green shoe", "dividen", "waran", "rights issue",
    "penambahan modal", "pengurangan modal", "emiten baru",
    "listing baru", "suspensi", "ipo",
]


def is_relevant(title: str) -> bool:
    if not title:
        return False
    t = title.lower()
    for kw in EXCLUDE:
        if kw in t:
            return False
    for kw in INCLUDE:
        if kw in t:
            return True
    return False


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {"last_ids": [], "enriched_ids": []}


def save_state(state: dict):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    json.dump(state, open(STATE_FILE, "w"))


# ─── Chroma ──────────────────────────────────────────────────────────────────────
def init_chroma():
    """Initialize Chroma DB with sentence-transformers embedding."""
    os.makedirs(CHROMA_PATH, exist_ok=True)
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    model = SentenceTransformer(EMBED_MODEL)

    try:
        col = client.get_or_create_collection(
            name="idx_actions",
            metadata={"description": "IDX Corporate Actions"}
        )
    except Exception:
        client.delete_collection("idx_actions")
        col = client.get_or_create_collection(
            name="idx_actions",
            metadata={"description": "IDX Corporate Actions"}
        )

    return client, col, model


def store_in_chroma(col, model, items: list):
    """Store corporate actions in vector DB with embeddings."""
    if not items:
        return

    # Deduplicate by ID
    seen = set()
    unique = []
    for item in items:
        iid = item.get("Id", "")
        if iid and iid not in seen:
            seen.add(iid)
            unique.append(item)

    if len(unique) < len(items):
        print(f"[*] Chroma: deduped {len(items)} → {len(unique)}")

    doc_texts = [f"[{i.get('Code', '').strip()}] {i.get('Title', '').strip()}" for i in unique]
    embeddings = model.encode(doc_texts, show_progress_bar=False)

    ids = [i.get("Id", "") for i in unique]
    metas = [{
        "code": i.get("Code", "").strip(),
        "title": i.get("Title", "").strip(),
        "date": i.get("PublishDate", ""),
        "type": "corporate_action",
    } for i in unique]

    col.upsert(
        ids=ids,
        documents=doc_texts,
        embeddings=[[float(x) for x in e] for e in embeddings],
        metadatas=metas,
    )
    print(f"[*] Chroma: stored {len(unique)} (384-dim embeddings)")


def search_chroma(col, model, query: str, n: int = 5) -> list:
    """Semantic search in Chroma."""
    emb = model.encode([query])
    try:
        res = col.query(
            query_embeddings=[[float(x) for x in emb[0]]],
            n_results=n,
            include=["metadatas", "distances"],
        )
        return res.get("metadatas", [[]])[0]
    except Exception as e:
        print(f"[!] Chroma search error: {e}")
        return []


# ─── Tavily ──────────────────────────────────────────────────────────────────
def enrich_with_tavily(col, model, code: str, title: str) -> dict:
    """Enrich with web search and past actions."""
    client = TavilyClient(api_key=TAVILY_KEY)
    query = f"{code} {title} Indonesia stock 2026"

    try:
        result = client.search(
            query,
            max_results=3,
            include_answer=True,
        )

        answer = result.get("answer", "")
        sources = [r["url"] for r in result.get("results", [])[:3]]

        past = search_chroma(col, model, f"{code} {title}", n=3)
        past_count = len([p for p in past if p.get("code") == code])

        return {
            "tavily_answer": answer[:400] if answer else "",
            "sources": sources,
            "past_count": past_count,
        }
    except Exception as e:
        print(f"[!] Tavily error: {e}")
        return {"tavily_answer": "", "sources": [], "past_count": 0}


# ─── IDX Fetch ──────────────────────────────────────────────────────────────
def fetch_recent(max_pages: int = 5, page_size: int = 50) -> list:
    items = []
    for page in range(max_pages):
        url = (
            f"{BASE_URL}/primary/NewsAnnouncement/GetAllAnnouncement"
            f"?pageSize={page_size}&pageNumber={page}&kodeEmiten="
        )
        try:
            resp = requests.get(
                url,
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Referer": "https://www.idx.co.id/id/perusahaan-tercatat/keterbukaan-informasi/",
                },
                impersonate="chrome",
                timeout=30,
            )
            if resp.status_code != 200:
                break
            data = resp.json()
            page_items = data.get("Items", [])
            if not page_items:
                break
            items.extend(page_items)
        except Exception as e:
            print(f"[!] Page {page} error: {e}")
            break
    return items


# ─── Telegram ────────────────────────────────────────────────────────────────
def send_telegram(message: str) -> bool:
    if not TELEGRAM_BOT_TOKEN:
        print("[*] No Telegram token — printing only")
        print(message)
        return False
    import urllib.request
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read()).get("ok", False)
    except Exception as e:
        print(f"[!] Telegram error: {e}")
        return False


# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    print(f"[{'=' * 50}]")
    print(f"[*] IDX Monitor v2 — {datetime.now()}")
    print(f"[{'=' * 50}]")

    client, col, model = init_chroma()
    state = load_state()
    last_ids = set(state.get("last_ids", []))

    all_items = fetch_recent(max_pages=5, page_size=50)
    print(f"[*] Fetched: {len(all_items)} disclosures")

    if not all_items:
        print("[!] No items fetched")
        return

    new_items = [i for i in all_items if i.get("Id", "") not in last_ids]
    relevant = [i for i in new_items if is_relevant(i.get("Title", ""))]
    print(f"[*] New: {len(new_items)} | Relevant: {len(relevant)}")

    # Track which item IDs we've already enriched (never process same ID twice)
    enriched_ids = set(state.get("enriched_ids", []))
    
    # Remove from relevant if already enriched before
    already_enriched = [i for i in relevant if i.get("Id", "") in enriched_ids]
    to_enrich = [i for i in relevant if i.get("Id", "") not in enriched_ids]
    
    if already_enriched:
        print(f"[*] Already enriched (skipping): {len(already_enriched)}")
        for i in already_enriched:
            print(f"  ⏭ [{i.get('Code','').strip()}] {i.get('Title','')[:60]}")
    
    print(f"[*] To enrich this run: {len(to_enrich)}")

    store_in_chroma(col, model, new_items)

    if not to_enrich:
        print("[*] No new relevant corporate actions to process.")
        save_state({
            "last_ids": [i.get("Id", "") for i in all_items[:100]],
            "enriched_ids": list(enriched_ids),
        })
        return

    header = (
        f"📊 <b>Keterbukaan Informasi IDX</b>\n"
        f"🕐 {datetime.now().strftime('%d %b %Y, %H:%M')} WIB\n"
        f"📁 {len(to_enrich)} aksi korporasi baru\n"
        f"{'─' * 25}\n"
    )

    messages = []
    for item in to_enrich:
        code = item.get("Code", "").strip()
        title = item.get("Title", "").strip()
        date = item.get("PublishDate", "")
        try:
            dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
            time_str = dt.strftime("%H:%M")
        except Exception:
            time_str = date[11:16] if len(date) > 16 else ""

        extra = enrich_with_tavily(col, model, code, title)

        # Extract PDF if available
        pdf_info = ""
        pdf_url = item.get("PDFUrl", "") or item.get("LinkUrl", "")
        if pdf_url and pdf_url.lower().endswith(".pdf"):
            try:
                pdf_text = fetch_pdf_text(pdf_url, max_pages=PDF_MAX_PAGES)
                key_info = extract_key_info(pdf_text)
                if key_info.get("dates") or key_info.get("amounts"):
                    parts = []
                    if key_info.get("dates"):
                        parts.append(f"📅 {key_info['dates'][0]}")
                    if key_info.get("amounts"):
                        parts.append(f"💰 {key_info['amounts'][0]}")
                    if key_info.get("codes"):
                        parts.append(f"📌 {', '.join(key_info['codes'][:3])}")
                    pdf_info = " | ".join(parts)
            except Exception as e:
                pdf_info = f"[PDF error: {str(e)[:30]}]"

        msg = f"📋 [{time_str}] - [{code}]\n{title}"
        if pdf_info:
            msg += f"\n📑 {pdf_info}"
        if extra["tavily_answer"]:
            msg += f"\n\n🔍 <i>{extra['tavily_answer']}</i>"
        if extra["sources"]:
            msg += "\n📎 Sources:"
            for src in extra["sources"][:2]:
                msg += f"\n  → {src[:60]}"
        if extra["past_count"] > 0:
            msg += f"\n📈 ({extra['past_count']}x sebelumnya)"

        messages.append(msg)
        time.sleep(0.5)

    # Send
    msg = header + "\n".join(messages)
    if len(msg) <= 4000:
        send_telegram(msg)
    else:
        parts = [header]
        for m in messages:
            if len(parts[-1]) + len(m) + 2 > 4000:
                parts.append(m)
            else:
                parts[-1] += "\n" + m
        for p in parts:
            send_telegram(p)
            time.sleep(1)

    # Mark all relevant as enriched
    for i in relevant:
        enriched_ids.add(i.get("Id", ""))
    
    save_state({
        "last_ids": [i.get("Id", "") for i in all_items[:100]],
        "enriched_ids": list(enriched_ids),
    })
    print(f"[*] Done! {len(to_enrich)} new corporate actions sent.")


if __name__ == "__main__":
    main()
