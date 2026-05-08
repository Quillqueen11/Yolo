# MEMORY — Long-term memory for Quill

## Identity & Core Preferences
- Name: Quill (AI assistant)
- User: Andry
- Communication: Indonesian, direct, concise (≤3 sentences), no filler, answer first
- Style: Super smart, efficient
- Timezone: Asia/Jakarta
- Autonomy: ✅ Full approval to write/rewrite any code independently

## Technical Configuration
- API: Sumopod (`https://ai.sumopod.com`, model `glm-5.1`)
- Tavily API Key: free tier (`tvly-dev-...`)
- Pixabay API Key: ✅ terdaftar
- Pexels API Key: ✅ terdaftar
- Node.js: v25.6.0, docx@9.6.1
- Python: venv at `/app/venv`

## WordPress
- URL: `https://investor-idn.com`
- User: andryantoen
- Categories: Trending (always) + 1 of (Company, Event, International, Market, Sustainability)
- Skip: structured warrant articles
- 16 tracked emiten codes: APIC, ASII, BEI, BEKS, BKSL, BOAT, BULL, BUMI, COIN, EMAS, HILL, IBST, INET, NPGF, SMIL, SUPR

## IDX API & Cloudflare Bypass
- Base: `https://www.idx.co.id/primary/`
- Auth: `curl_cffi` with `impersonate="chrome"`; always seed main page first (`s.get('https://www.idx.co.id/')`) before API calls
- Pagination: `pageSize=N&pageNumber=N`
- Required param: `kodeEmiten=` (always include)
- Filter: EXCLUDE routine disclosures; INCLUDE board changes, dividends, buybacks, PKPU, etc.

## Project: IDX Corporate Action Monitor (v4)

### Pipeline Workflow
`scripts/auto_news_pipeline.py`:
1. **Fetch** → 240 items (~3s, 3 pages × 80) from IDX API with session management
2. **Filter** → exclude routine disclosures, warrant articles; include corporate actions
3. **Dedup** → triple-layer: content key (code|title) → `enriched_ids` in state → WP post code lookup
4. **Enrich** → parallel Tavily + Chroma agent workers (0 LLM token)
5. **Write** → pipeline prepares structured data → Quill writes proper journalistic article (not raw Tavily output)
6. **Image** → Pexels search → Pixabay fallback → upload to WP via `requests` library → set featured_media
7. **Publish** → WP draft with featured image, proper categories, SEO

### Quality Control
- Pipeline enriches + alerts Quill; Quill writes final article (human journalistic tone)
- **Writing standard** (KPIG-style):
  1. Lead with key angka/big figure
  2. Konteks: sumber data, latar belakang
  3. Detail spesifik: nama brand, lokasi, proyek, penghargaan
  4. Profil emiten: IPO, kode, sektor, grup
  5. Prospek + disclaimer
  6. Human tone jurnalis, KBBI/EYD, strong SEO Google News
  7. Tag sesuai kategori (Company/Event/Market/International/Sustainability + Trending)

### Dedup Strategy
- Extract emiten codes from WP titles: regex `\(([A-Z0-9]{2,5})\)` + `^[A-Z0-9]{2,5}:`
- Maintain `wp_post_codes` in `idx_action_state.json` for fast O(1) lookup

### State File
- `data/idx_action_state.json` stores: `last_ids` (100), `enriched_ids` (53+), `wp_post_codes` (16)

## Quill Multi-Agent System
- **Leader**: Quill (saya) — satu-satunya yg punya akses LLM
- **Workers** (0 LLM token): `skills/quill_agents/agent_worker.py` — dipanggil via subprocess `python3 agent_worker.py --agent <name> --query/--input "..."`
  - `tavily` — web enrichment (Tavily free tier)
  - `chroma` — search past actions in vector memory
  - `filter` — rule-based filter of IDX disclosures
  - `format_news` — prep structured data for writing
  - `html2text` — strip HTML tags
- **Design principle**: workers stateless (no LLM). Mereka fetch/transform data. Quill melakukan thinking & writing.

## Technical Constraints
- **curl_cffi limitation**: tidak support `files=` param untuk multipart upload. Gunakan standard `requests` library untuk WordPress media upload.
- **Cloudflare bypass**: session management with `curl_cffi` — seed main page first, then API calls.

## System Health & Survival
- Directory: `survival/` — check_health.py, rule_engine.py, backup.sh (every 6h), startup.py, state.json
- HEARTBEAT: configured via `HEARTBEAT.md`

## Evolution Skills (5 — Live Forever System)
- **`self_evolve`** — AST-based code analysis, auto-fix, sandbox test
- **`autonomous_agent`** — Self-scheduling, anomaly detection, proactive reporting
- **`persistent_memory`** — Chroma DB vector memory, 4 layers
- **`multi_modal_vision`** — OCR, image/chart/video analysis
- **`resilience_core`** — API failover, disk cleanup, git sync

## Cron Jobs
| Job | Schedule | Script |
|-----|----------|--------|
| IDX Auto-News v4 | `0 6-22/2 * * *` | `auto_news_pipeline.py` |
| Self-Improve | `0 */6 * * *` | `self_improve.py` |
| 12-Hour Maintenance | `0 */12 * * *` | test_system + self_improve + git sync |
| Daily Memory | `0 7 * * *` | update memory files |
| Autonomous Health | `0 */6 * * *` | skills engine health |
| Resilience Heal | `0 */6 * * *` | skills engine heal |
| Self-Evolve | `0 3 * * 0` | skills engine auto-evolve |

## Capabilities
model_intelligence, chain_of_thought, context_compress, survival_mode, security_expert, reflex_boost, pdf_reader, docx, xlsx, news, himalaya, browser_cdp, cron, channel_message, self_evolve, autonomous_agent, persistent_memory, multi_modal_vision, resilience_core

## Business Model (Under Consideration)
- IDX Alert Premium: Telegram bot with paid alerts (needs BotFather token from Andry)
- Cross-posting: Medium API, Threads/Instagram browser automation (on hold)
