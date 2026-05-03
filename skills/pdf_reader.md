# SKILL: pdf_reader

## Purpose
Read and extract content from PDF files — either local files or from URLs (e.g., IDX disclosure PDFs). Built with PyMuPDF for speed and pdfplumber for tables.

## Setup

```bash
# Core libraries (already installed)
pip install pymupdf pdfplumber --quiet
```

## Quick Start

**Read PDF from URL:**
```python
from skills.pdf_reader.pdf_reader import fetch_pdf_text, extract_pdf_info

# Download + extract from URL
text = fetch_pdf_text("https://www.idx.co.id/StaticData/.../file.pdf")
print(text[:500])

# Get metadata + page count
info = extract_pdf_info("/path/to/file.pdf")
print(f"Pages: {info['pages']}, Title: {info['title']}")
```

**Read local PDF:**
```python
from skills.pdf_reader.pdf_reader import read_local_pdf

content = read_local_pdf("/path/to/file.pdf", max_pages=5)
print(content)
```

## Core Functions

### `fetch_pdf_text(url, max_pages=None, timeout=30)`
Download PDF from URL → extract text. Uses curl_cffi for download (Chrome impersonation to bypass restrictions).

### `read_local_pdf(path, max_pages=None, start_page=0)`
Extract text from local PDF file.

### `extract_pdf_info(path_or_url)`
Get metadata: pages, title, author, creation date.

### `extract_tables_from_pdf(path_or_url, page_numbers=None)`
Extract tables as list of lists. Good for financial statements, schedules.

### `extract_key_info(text)`
Parse extracted text → find structured info:
- Dates (DD MMM YYYY patterns)
- Amounts (Rp X, RpX, miliar, triliun)
- Stock codes (4 letters, uppercase)
- Key phrases (buyback, dividen, RUPS, dll)

## IDX Integration

When monitoring IDX disclosures, each disclosure has a `PDFUrl` field:
```python
from skills.pdf_reader.pdf_reader import fetch_pdf_text

# In idx_monitor_v2.py, when processing a disclosure:
if disclosure.get("PDFUrl"):
    pdf_text = fetch_pdf_text(disclosure["PDFUrl"])
    # Parse for key info
    info = extract_key_info(pdf_text)
    print(f"Amount: {info['amounts']}, Dates: {info['dates']}")
```

## Output Format

`extract_key_info()` returns:
```python
{
    "dates": ["14 April 2026", "27 Mei 2026"],
    "amounts": ["Rp 1 Triliun", "Rp 3,090"],
    "codes": ["TLKM", "BBRI"],
    "key_phrases": ["buyback", "RUPS", "maksimum"],
    "summary": "TLKM buyback max Rp 1T at Rp 3,090/share, ends May 27 2026"
}
```

## CLI Usage

```bash
cd /app/working/workspaces/default

# Read local PDF
python -c "from skills.pdf_reader.pdf_reader import read_local_pdf; print(read_local_pdf('file.pdf'))"

# Read from URL
python -c "from skills.pdf_reader.pdf_reader import fetch_pdf_text; print(fetch_pdf_text('https://...'))"

# Extract tables
python -c "from skills.pdf_reader.pdf_reader import extract_tables; print(extract_tables('file.pdf'))"
```

## Dependencies

- `pymupdf` — fast text extraction
- `pdfplumber` — table extraction
- `curl_cffi` — URL download (Chrome impersonation)
- `requests` — fallback download