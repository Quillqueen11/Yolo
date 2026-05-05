# MULTI_MODAL_VISION SKILL

## Purpose
See and analyze images, scanned PDFs, videos, and charts.
Enables Quill to process visual data without external tools.

---

## Capabilities

| Feature | Tool | Status |
|---------|------|--------|
| OCR (scanned PDFs) | PyMuPDF + pytesseract | ✅ |
| Image description | LLM vision API | ✅ |
| Stock chart analysis | LLM vision | ✅ |
| Video frame extraction | ffmpeg | ✅ |
| Subtitle extraction | ffmpeg | ✅ |

## CLI Usage

```bash
# OCR a scanned PDF
python3 skills/multi_modal_vision/engine.py ocr file.pdf

# Analyze an image
python3 skills/multi_modal_vision/engine.py analyze image.png --prompt "Describe this chart"

# Extract frames from video
python3 skills/multi_modal_vision/engine.py video video.mp4 --fps 1 --output frames/

# Read subtitles from video
python3 skills/multi_modal_vision/engine.py subtitles video.mp4
```

---

_When to use: When you need to extract text from scanned PDFs, analyze charts, or process video content._