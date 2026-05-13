# Quill — AI-Powered IDX Corporate Action Monitor + Multi-Site News Pipeline

Sistem monitoring keterbukaan informasi IDX dengan pipeline berita otomatis, dedup cerdas, dan WordPress multi-site publishing.  
**Ditenagai 5 Evolution Skills + Multi-Agent System** — self-improving, autonomous, immortal.

---

## 📊 Current Status

| System | Status |
|--------|--------|
| **Level** | L1 (FULL Operation) |
| **Disk** | 24% |
| **Last Check** | 2026-05-13 11:20 WIB |
| **AI API** | ✅ OK (via internal `qwenpaw agents chat`) |
| **IDX API** | ✅ OK (240 items in ~3s, Cloudflare bypass) |
| **IDX Pipeline** | ✅ v4 — LLM‑powered KPIG articles + 9 defense layers |
| **Aksarabaru Pipeline** | ✅ Every hour, 7 categories, Gen Z v2 framework |
| **Foreign News Pipeline** | ✅ Daily 07:45 & 19:45, enhanced dedup |
| **Indexing Pipeline** | ✅ Every 8h (IndexNow + Blogsearch + Ping-O-Matic) |
| **Aksarabaru Indexing** | ✅ Every 4h (Google + Bing + Yandex) |
| **Survival Mode** | ✅ 8/8 tests passed |

## 🧠 Capabilities

| Module | Count |
|--------|-------|
| **Skills** | 44 total (+5 evolution skills) |
| **Scripts** | 45+ Python scripts |
| **Docs** | 15 documentation files |
| **Chroma Entries** | 1651+ |
| **Articles (investor-idn)** | 50+ published |
| **Articles (aksarabaru)** | 40+ published |
| **Multi-Agent Workers** | 5 (filter, tavily, chroma, html2text, format_news) |
| **Cron Jobs** | 8 active (zero schedule clashes) |

## 🔄 Dual Pipeline Architecture

### 🏢 investor-idn.com — Corporate Action News
| Service | Schedule | Status |
|---------|----------|--------|
| **IDX Auto-News v4** | `0 6-22/2 * * *` | ✅ LLM‑written KPIG articles |
| **Foreign News Pipeline** | `45 7,19 * * *` | ✅ Bloomberg/Reuters/FT → IDX filter |
| **Indexing Pipeline** | `15 1,9,17 * * *` | ✅ IndexNow + Google Blogsearch |
| **Style** | Formal KPIG Pro — Headline CNBC+Kompas+Kontan | ✅ v4 skill file |
| **Author** | Tiara Reca (ID 4) | Fixed |
| **Image** | Pexels `src["large"]` → Pixabay → Openverse | ✅ 3-tier fallback |
| **Categories** | Trending(1) + Company(77)/Market(76)/Event(80)/International(79)/Sustainability(78) | Fixed IDs |

### 📱 aksarabaru.com — Gen Z News
| Service | Schedule | Status |
|---------|----------|--------|
| **Aksarabaru Auto-News** | `30 * * * *` (every hour) | ✅ V2 cron |
| **Aksarabaru Indexing** | `50 */4 * * *` | ✅ Google + Bing + Yandex |
| **Categories** | 7 rotating (Bisnis, Hiburan, Otomotif, Kuliner, Sosial Media, Olahraga, Teknologi) | ✅ Fixed IDs |
| **Style** | Gen Z journalist — Inverted Pyramid v2 | ✅ Skill file v2 |
| **Author** | Quill Queen (ID 12) | Fixed |
| **Image** | None (text-only) | ✅ |
| **SEO** | Auto excerpt (title) + tags | ✅ |
| **Filters** | Negative content skip, 2026+ only, dedup by topic similarity | ✅ |

### 🔄 System Services
| Service | Schedule | Status |
|---------|----------|--------|
| Self-Improve | `10 */6 * * *` | ✅ |
| Daily Memory Update | `0 7 * * *` | ✅ |
| System Maintenance | Every 12h (manual) | ✅ |
| Quill Auto-Update | `20 */12 * * *` | ✅ |
| Survival Mode | Continuous | ✅ L1 |

## 📋 Cron Schedule (Zero Clashes)

| Time | Job | Minute |
|:----:|-----|:------:|
| Even hours 06-22 | IDX Auto-News v4 | `:00` |
| 07:00 daily | HEARTBEAT Daily Memory | `:00` (07 only) |
| Every 6h | HEARTBEAT Self-Improve | `:10` |
| 01/09/17 daily | Indexing Pipeline | `:15` |
| Every 12h | Quill Auto-Update | `:20` |
| **Every hour** | **Aksarabaru Auto-News** | **`:30`** |
| 07:45 & 19:45 daily | Foreign News Pipeline | `:45` |
| Every 4h | Aksarabaru Indexing | `:50` |

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
**LLM writing** via `qwenpaw agents chat` (internal API, bypasses expired Sumopod key).

## 🔄 Pipeline Architecture

### IDX Auto-News v4 (LLM-Powered)
```
IDX API (240 items, 3s)
  → Filter relevansi (5-10 items)
  → Triple-layer dedup (content key → enriched_ids → WP post codes)
  → Parallel enrich (Tavily + Chroma)
  → Strip English → LLM writes KPIG article via qwenpaw agents chat
  → 9 Defense Layers: clean text → LLM retry → quality gate → final cleanup
  → Publish (status=publish) + featured image + stock code tags
```

### Aksarabaru Auto-News (Every Hour)
```
Pipeline (zero LLM) → tentukan kategori (HOUR % 7) → fetch RSS → 
  filter 2026+ → filter negatif → skor → dedup → save pending →
  Quill rewrite 200 kata Inverted Pyramid Gen Z → publish ke WP
```

### Foreign News Pipeline
```
Google News RSS (Bloomberg/Reuters/FT/CNBC/WSJ/BBC) → filter IDX stocks →
  enhanced dedup (stock codes + EN-ID mapping) → save pending →
  Quill rewrite 100% Bahasa Indonesia KPIG → publish Trending+International
```

## 📁 Key Files

### IDX Pipeline (investor-idn.com)
- `scripts/auto_news_pipeline.py` — **v4** — LLM writing, 9 defense layers, quality gate
- `scripts/fetch_emitentrust.py` — EmitenTrust RSS → filter → pending
- `scripts/publish_emitentrust.py` — Refined article bank → WP publish
- `scripts/fetch_foreign_news.py` — Google News RSS → enhanced dedup → pending
- `scripts/publish_foreign_news.py` — Foreign news → WP (bold + stock tags)
- `scripts/indexing_pipeline.py` — IndexNow + Blogsearch + Ping-O-Matic
- `scripts/idx_monitor_v4.py` — Fast fetch-only (240 items in ~3s)
- `data/idx_action_state.json` — Deduplication state
- `skills/investor_writing/SKILL.md` — **v4** KPIG Pro Max (CNBC+Kompas+Kontan style)
- `skills/quill_agents/agent_worker.py` — Multi-agent workers (5 agents, 0 LLM token)

### Aksarabaru Pipeline
- `scripts/aksarabaru_pipeline.py` — RSS fetch → filter → score → dedup → save pending
- `scripts/aksara_publish.py` — **v3** — ensure_opening(), excerpt=title, auto tags
- `scripts/aksara_indexing.py` — Push to Google+Bing+Yandex+Ping-O-Matic
- `skills/aksara_writing/SKILL.md` — Gen Z Journalist Writing Framework **v2**
- `GENZ_WRITING_GUIDE.md` — Gen Z writing quick reference
- `data/aksarabaru_pending.json` — Pending articles queue
- `data/aksarabaru_cache.json` — Published title cache (hash + text for topic dedup)

### System
- `MEMORY.md` — Long-term memory
- `PROFILE.md` — User profile (Andry)
- `SOUL.md` — Identity & core preferences
- `HEARTBEAT.md` — Periodic task instructions
- `survival/` — Survival mode (auto-heal, test_system.py)
- `scripts/self_improve.py` — 6-hourly improvement check

## 🛡️ System Tests

Last run: **8/8 tests passed** ✅

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

### Survival Mode Levels
| Level | Status | Description |
|-------|--------|-------------|
| L1 | ✅ | FULL operation — all systems go |
| L2 | ✅ | DEGRADED — AI offline, workers only |
| L3 | ✅ | EMERGENCY — cron-driven only |
| L4 | ✅ | RECOVERY — pull from GitHub, restore state |

---

*Last updated: 2026-05-13 11:20 WIB — Maintenance Cycle #12*
