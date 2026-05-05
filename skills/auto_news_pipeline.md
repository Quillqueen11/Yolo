# AUTO NEWS PIPELINE SKILL

## Purpose
Automated news generation pipeline — from data collection to polished article.

---

## Architecture: 4-Layer System

```
INPUT → L1: COLLECT → L2: DRAFT → L3: QC → L4: POLISH → OUTPUT
```

### Layer 1 — Data Collection
Sumber data yang sudah siap:
- **IDX API** (keterbukaan informasi, corporate actions)
- **YouTube scraper** (channel analytics, trending topics)
- **Tavily web search** (berita, tren, kompetitor)
- **Browser scraping** (portal berita, Google Trends)

### Layer 2 — Fast Draft Generation
```python
def generate_draft(data, tone="cnbc"):
    prompt = f"""Buat draft berita dari data berikut:
{data}
Tone: {tone} (CNBC Indonesia)
Struktur: Judul → Lead → Isi → Analisis"""
    return call_llm(prompt)
```

### Layer 3 — Quality Gate
```python
def quality_check(article):
    checks = [
        len(article) > 300,          # Minimum length
        'disclaimer' in article.lower(),  # Has disclaimer
        not is_duplicate(article),    # No duplicate
        has_data_points(article),     # Has facts/data
        verify_numbers(article),      # No hallucinated numbers
    ]
    return all(checks), [c for c in checks if not c]
```

### Layer 4 — Polish
```python
def polish_article(draft, tone="cnbc"):
    prompt = f"""Polish artikel berikut. Standar:
- Bahasa Indonesia baku (EYD V)
- Fakta akurat
- Alur naratif
- Tone: {tone}
- Panjang: 500-900 kata

DRAFT: {draft}"""
    return call_llm_advanced(prompt)
```

---

## Pipeline Lengkap

```python
def run_pipeline(source="idx", max_articles=5):
    articles = []
    
    if source == "idx":
        raw = fetch_idx_disclosures()
    elif source == "youtube":
        raw = scrape_youtube_trending()
    elif source == "web":
        raw = tavily_search("berita pasar modal indonesia")
    
    topics = cluster_topics(raw)
    
    for topic in topics[:max_articles]:
        draft = generate_draft(topic)
        passed, fails = quality_check(draft)
        if not passed:
            draft = fix_article(draft, fails)
        final = polish_article(draft)
        articles.append(final)
    
    return articles
```

---

## Integrasi

```
auto_news_pipeline → content_agency (strategy)
                   → deep_content_analysis (audience)
                   → image_recognition (thumbnail)
                   → wordpress_publisher (publish)
                   → quality_gate (QC)
```

---

## Quick Run

```bash
python3 -c "
from skills.auto_news_pipeline import run_pipeline
articles = run_pipeline(source='idx', max_articles=3)
for a in articles:
    print(a['title'])
"
```

---

_When to use: Generate news articles automatically from data sources._