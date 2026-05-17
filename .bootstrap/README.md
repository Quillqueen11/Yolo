# Quill — AI-Powered IDX Corporate Action Monitor

Sistem monitoring keterbukaan informasi IDX dengan pipeline berita otomatis, dedup cerdas, dan WordPress publishing.  
**Ditenagai 5 Evolution Skills + Multi-Agent System** — self-improving, autonomous, immortal.

---

## 📊 Current Status

| System | Status |
|--------|--------|
| **Level** | L1 (FULL Operation) |
| **Disk** | 26% |
| **Last Check** | 2026-05-17 12:20 WIB |
| **AI API** | ✅ OK |
| **Pipeline** | ✅ v4 (240 items in 3s) |

## 🧠 Capabilities

| Module | Count |
|--------|-------|
| **Skills** | 42 total (+5 evolution skills) |
| **Scripts** | 30+ Python scripts |
| **Docs** | 14 documentation files |
| **Chroma Entries** | 1651+ |
| **News Articles** | 15+ published |
| **SCPI Covered** | ✅ Go Private Rp29.000 |
| **Multi-Agent Workers** | 5 (filter, tavily, chroma, html2text, format_news) |

## 🔄 Running Services

| Service | Schedule | Status |
|---------|----------|--------|
| **IDX Auto-News v4** | Every 2h (06:00-22:00 WIB) | ✅ **NEW** |
| Self-Improve | Every 6h | ✅ Active |
| Daily Memory Update | Daily 07:00 | ✅ Active |
| System Maintenance | Every 12h | ✅ Active |
| Autonomous Health | Every 6h | ✅ Active |
| Resilience Heal | Every 6h | ✅ Active |
| Self-Evolve | Weekly (Sun 03:00) | ✅ Active |

## 🆕 Multi-Agent System

```
Quill (Leader — LLM) ──→ Agent Workers (0 token, subprocess)
    │
    ├── filter    → Rule-based disclosure filter
    ├── tavily    → Web enrichment (Tavily free tier)
    ├── chroma    → Vector DB search (past actions)
    ├── html2text → HTML tag stripper
    └── format_news → Structured data prep
```

**Penghematan token:** Semua agent worker jalan via subprocess, 0 LLM token.  
**Saya (Quill) pakai LLM hanya untuk nulis berita dan refine.**

## 🆕 Auto-News Pipeline (v4)

```
Angka ➡️
Fetch IDX API (240 items, 3 detik)
  ➡️ Filter relevansi (5-10 items)
  ➡️ Cek state + WordPress dedup
  ➡️ Enrich paralel (Tavily + Chroma)
  ➡️ Publish draft ke WordPress
  ➡️ Simpan state (tidak publish ulang)
```

Keunggulan:
- Session management (seed main page → bypass Cloudflare)
- WordPress dedup by emiten code (cek existing posts)
- Parallel enrich via ThreadPoolExecutor
- State + WP code tracking (tidak ada duplikasi)

## 📁 Key Files

- `scripts/auto_news_pipeline.py` — **Pipeline utama v4** (fetch → filter → enrich → WP)
- `skills/quill_agents/agent_worker.py` — **Multi-agent workers** (5 agents, 0 LLM token)
- `scripts/idx_monitor_v4.py` — Fast fetch-only (240 items in ~3s)
- `data/idx_action_state.json` — Deduplication state (53 enriched, 16 WP codes)
- `data/chroma_db/` — Vector DB for dedup

## 📝 Recent News Articles

| Article | Status |
|---------|--------|
| TLKM Buyback Rp1T | ✅ Published |
| KPIG Q1 Laba +55.8% | ✅ Published |
| APLN Volatilitas 16% | ✅ Published |
| BSDE Prapenjualan Rp2.54T | ✅ Published |
| NUSA Suspensi Seluruh Pasar | ✅ Published |
| INET Dirut & Komisaris Mundur | ✅ Published |
| IBST Amankan Sub Limit Kredit Rp1T | ✅ Published |
| SUPR Go Private Rp45.000 | ✅ Published |
| HILL Saham Anjlok 66% PKPU | ✅ Published |
| BOAT Tambah Kapal Baru US$22 Juta | ✅ Published |
| NPGF Kontrak Rp217 Miliar | ✅ Published |
| MAPI Pacific Universal Akuisisi 51% | ✅ Published |
| RATU Dividen Rp122,17 M | ✅ Published |
| PACK Pemegang Saham Baru Borong | ✅ Published |
| LKH Borong 5,2 Juta Saham DILD | ✅ Published |

## 🛡️ System Tests

Last run: `8/8 tests passed` ✅ (2026-05-17 12:20 WIB)

| Test | Status |
|------|--------|
| Health Check | ✅ |
| Backup System | ✅ |
| Rule Engine | ✅ |
| Startup Recovery | ✅ |
| Data Integrity | ✅ |
| State Consistency | ✅ |
| Log System | ✅ |
| Failure Recovery | ✅ |

---

*Last updated: 2026-05-17 12:20 WIB*

