# Quill — AI-Powered IDX Corporate Action Monitor + Multi-Site News Pipeline

Sistem monitoring keterbukaan informasi IDX dengan pipeline berita otomatis, dedup cerdas, dan WordPress multi-site publishing.  
**Ditenagai 5 Evolution Skills + Multi-Agent System** — self-improving, autonomous, immortal.

---

## 📊 Current Status

| System | Status |
|--------|--------|
| **Level** | L1 (FULL Operation) |
| **Disk** | 20% |
| **Last Check** | 2026-05-09 11:00 WIB |
| **AI API** | ✅ OK |
| **IDX Pipeline** | ✅ v4 (240 items in 3s) |
| **Aksarabaru Pipeline** | ✅ Every hour, 7 categories |
| **Gen Z Writing Skill** | ✅ v2 — Inverted Pyramid, Anti-AI, Quality Check |

## 🧠 Capabilities

| Module | Count |
|--------|-------|
| **Skills** | 43 total (+5 evolution skills) |
| **Scripts** | 30+ Python scripts |
| **Docs** | 15 documentation files |
| **Chroma Entries** | 1651+ |
| **News Articles (investor-idn)** | 16+ published |
| **News Articles (aksarabaru)** | 8+ published |
| **Multi-Agent Workers** | 5 (filter, tavily, chroma, html2text, format_news) |

## 🔄 Dual Pipeline Architecture

### 🏢 investor-idn.com — IDX Corporate Action News
| Service | Schedule | Status |
|---------|----------|--------|
| **IDX Auto-News v4** | Every 2h (06:00-22:00 WIB) | ✅ Active |
| **Style** | Formal, human tone, KBBI/EYD | KPIG-style structure |
| **Author** | Tiara Reca (ID 4) | — |
| **Image** | Pexels → Pixabay → Openverse | ✅ 3-tier fallback |

### 📱 aksarabaru.com — Gen Z News
| Service | Schedule | Status |
|---------|----------|--------|
| **Aksarabaru Auto-News** | Every hour (`30 * * * *`) | ✅ Active |
| **Categories** | 7 rotating (Bisnis, Hiburan, Otomotif, Kuliner, Sosial Media, Olahraga, Teknologi) | ✅ |
| **Style** | Gen Z journalist — Inverted Pyramid | ✅ v2 framework |
| **Author** | Quill Queen (ID 12) | — |
| **Image** | None (no featured image) | ✅ |
| **SEO** | Auto excerpt + tags from publish script v2 | ✅ |
| **Filters** | Negative content skip, 2026+ only, dedup by topic similarity | ✅ |

### 🔄 Other Services
| Service | Schedule | Status |
|---------|----------|--------|
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

## 📱 Aksarabaru Pipeline

Setiap jam:
```
Pipeline → tentukan kategori (jam % 7) → fetch RSS → filter 2026+ → 
  filter negatif → skor → dedup (hash + topic similarity) → save pending →
  Quill rewrite Inverted Pyramid 200 kata Gen Z → publish ke WP
```

### Gen Z Writing Framework (v2)
- **Inverted Pyramid**: LEAD1 (5W1H) → LEAD2 (relevansi) → DETAIL (fakta) → TAIL
- **Anti-AI**: No passive voice, no uniform length, no repetition
- **Quality Check**: 5-point score before publish (min score 4/5)
- **Skill file**: `skills/aksara_writing/SKILL.md`

## 📁 Key Files

### IDX Pipeline (investor-idn.com)
- `scripts/auto_news_pipeline.py` — Pipeline utama v4 (fetch → filter → enrich → WP)
- `skills/quill_agents/agent_worker.py` — Multi-agent workers (5 agents, 0 LLM token)
- `scripts/idx_monitor_v4.py` — Fast fetch-only (240 items in ~3s)
- `data/idx_action_state.json` — Deduplication state
- `data/chroma_db/` — Vector DB for dedup

### Aksarabaru Pipeline (aksarabaru.com)
- `scripts/aksarabaru_pipeline.py` — RSS fetch → filter → score → dedup → save pending (zero LLM)
- `scripts/aksara_publish.py` — Publish script v2 with auto SEO excerpt + tags + validation
- `skills/aksara_writing/SKILL.md` — Gen Z Journalist Writing Framework v2
- `data/aksarabaru_pending.json` — Pending articles queue
- `data/aksarabaru_cache.json` — Published title cache (hash + text for topic dedup)

### System
- `MEMORY.md` — Long-term memory
- `GENZ_WRITING_GUIDE.md` — Gen Z writing quick reference
- `HEARTBEAT.md` — Periodic task instructions

## 📝 Recent Articles

### investor-idn.com (16+ articles)
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

### aksarabaru.com (8+ articles)
| Article | Category | Status |
|---------|----------|--------|
| Pertalite Mulai Hilang dari SPBU? | Otomotif | ✅ Published |
| Bansos Pangan Natuna | Kuliner | ✅ Published |
| Earphone & Kesehatan Telinga | Kuliner | ✅ Published |
| TikTok Platform Paling Populer 2026 | Sosial Media | ✅ Published |
| #KaburAjaDulu Viral di Medsos | Sosial Media | ✅ Published |
| Konten Viral RI Go International | Sosial Media | ✅ Published |

## 🛡️ System Tests

Last run: `8/8 tests passed` ✅

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

*Last updated: 2026-05-09 11:00 WIB*
