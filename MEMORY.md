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
### investor-idn.com
- URL: `https://investor-idn.com`, User: andryantoen
- Categories: Trending (always) + 1 of (Company, Event, International, Market, Sustainability)
- Skip: structured warrant articles
- Tracked emiten: APIC, ASII, BEI, BEKS, BKSL, BOAT, BULL, BUMI, COIN, EMAS, HILL, IBST, INET, NPGF, SMIL, SUPR

### aksarabaru.com
- URL: `https://aksarabaru.com`, User: Quill Queen (ID 12), Password: Langsung123
- App Password: DISABLED — use Basic Auth with user password
- 7 categories: Bisnis(3), Hiburan(6), Otomotif(7), Kuliner(5), Sosial Media(4), Olahraga(8), Teknologi(10)
- Writing: 200 words, Gen Z journalist style, conversational Indonesian (lihat `GENZ_WRITING_GUIDE.md`)
- Rotation: setiap jam bergantian (HOUR % 7)
- **WAJIB**: "aksarabaru.com - " di awal konten + "Jakarta" di artikel
- **SEO**: excerpt meta desc auto, tags auto dari category
- **Dedup**: similarity check (Jaccard 0.30) + stem matching

## IDX API & Cloudflare
- Base: `https://www.idx.co.id/primary/`
- Auth: `curl_cffi` with `impersonate="chrome"`; seed main page first before API calls
- Filter: EXCLUDE routine; INCLUDE board changes, dividends, buybacks, PKPU

## Pipelines
### IDX Auto-News (investor-idn.com)
Fetch 240 (3s) → Filter → Triple dedup → Parallel enrich (Tavily+Chroma) → Image (Pexels→Pixabay) → WP publish
- **Writing standard**: lead angka → konteks → detail spesifik → profil emiten → prospek → KBBI/EYD, human tone, strong SEO
- **Dedup**: content key → enriched_ids → WP post codes via regex `\(([A-Z0-9]{2,5})\)`
- **Script**: `scripts/auto_news_pipeline.py`

### Aksarabaru Auto-News
Setiap jam → tentukan kategori → fetch **Google News RSS** (primary) + portal → filter keyword → skor → dedup → simpan pending → Quill rewrite 200 kata Gen Z → WP publish (tanpa gambar)
- **Script**: `scripts/aksarabaru_pipeline.py` (fetch, zero LLM)
- **Publish**: `scripts/aksara_publish.py` (publish only, no image)
- **Quill writes**: via LLM — judul curiosity gap, 200 kata, gaya jurnalis Gen Z
- **Dedup**: title hash cache + WP existing check

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
| **Aksarabaru Auto-News** | **`30 * * * *`** |
| Self-Improve | `0 */6 * * *` |
| 12-Hour Maintenance | `0 */12 * * *` |
| Daily Memory | `0 7 * * *` |

## Capabilities
model_intelligence, chain_of_thought, context_compress, survival_mode, security_expert, reflex_boost, pdf_reader, docx, xlsx, news, himalaya, browser_cdp, cron, channel_message, evolution skills (5)

## Writing Style Separation — KRITIS!

### investor-idn.com (IDX auto-news)
- **Style**: Formal, human tone, KBBI/EYD
- **Struktur**: lead angka → konteks → detail spesifik → profil emiten → prospek
- **Framework**: Pipeline `auto_news_pipeline.py` — system prompt LLM untuk nulis
- **Referensi**: https://investor-idn.com/2026/05/04/laba-mnc-tourism-melompat-558-hotel-dan-resor-jadi-motor-pertumbuhan/
- **Author**: Tiara Reca (ID 4)
- **Image**: Pexels → Pixabay → Openverse
- **JANGAN GUNAKAN** Gen Z style, kata santai (lo/gue/banget), atau vocabulary aksarabaru

### aksarabaru.com (Auto-news every hour)
- **Style**: Gen Z journalist, santai, langsung, human
- **Struktur**: Inverted Pyramid (LEAD → DETAIL → TAIL)
- **Framework**: `skills/aksara_writing/SKILL.md` — system role jurnalis Gen Z 22 thn
- **Referensi**: GENZ_WRITING_GUIDE.md
- **Author**: Quill Queen (ID 12)
- **Image**: TANPA featured image
- **Wajib**: "aksarabaru.com - " di awal, "Jakarta" di konten
- **SEO**: excerpt auto, tags auto dari publish script v2
- **JANGAN GUNAKAN** gaya formal, struktur lead angka, atau profil emiten
