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
- Tavily: `tvly-dev-...`, Pexels: ✅, Pixabay: ✅
- Python: venv at `/app/venv`, Node: v25.6.0

## WordPress
- URL: `https://investor-idn.com`, User: andryantoen
- Categories: Trending (always) + 1 of (Company, Event, International, Market, Sustainability)
- Skip: structured warrant articles
- Tracked emiten: APIC, ASII, BEI, BEKS, BKSL, BOAT, BULL, BUMI, COIN, EMAS, HILL, IBST, INET, NPGF, SMIL, SUPR

## IDX API & Cloudflare
- Base: `https://www.idx.co.id/primary/`
- Auth: `curl_cffi` with `impersonate="chrome"`; seed main page first before API calls
- Filter: EXCLUDE routine; INCLUDE board changes, dividends, buybacks, PKPU

## Pipeline (auto_news_pipeline.py)
Fetch 240 (3s) → Filter → Triple dedup → Parallel enrich (Tavily+Chroma) → Image (Pexels→Pixabay) → Quill writes → WP draft
- **Writing standard**: lead angka → konteks → detail spesifik → profil emiten → prospek → KBBI/EYD, human tone, strong SEO
- **Dedup**: content key → enriched_ids → WP post codes via regex `\(([A-Z0-9]{2,5})\)`

## Multi-Agent System
- **Leader**: Quill (LLM access)
- **Workers** (0 token, subprocess): filter, tavily, chroma, html2text, format_news
- Workers fetch/transform; Quill thinks & writes

## Constraints
- curl_cffi: no `files=` for multipart → use `requests` for WP media upload
- Cloudflare: session management with curl_cffi, seed main page first

## Evolution Skills (5)
self_evolve, autonomous_agent, persistent_memory, multi_modal_vision, resilience_core

## Cron Jobs
| Job | Schedule |
|-----|----------|
| IDX Auto-News v4 | `0 6-22/2 * * *` |
| Self-Improve | `0 */6 * * *` |
| 12-Hour Maintenance | `0 */12 * * *` |
| Daily Memory | `0 7 * * *` |

## Capabilities
model_intelligence, chain_of_thought, context_compress, survival_mode, security_expert, reflex_boost, pdf_reader, docx, xlsx, news, himalaya, browser_cdp, cron, channel_message, evolution skills (5)

## Business Model (Consideration)
- IDX Alert Premium: Telegram bot paid alerts (needs BotFather token)
- Cross-posting: Medium/Threads/Instagram (on hold)
