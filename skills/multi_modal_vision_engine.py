#!/usr/bin/env python3
"""
multi_modal_vision engine — OCR, image analysis, video processing.
"""
import os, sys, json, subprocess, tempfile
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent.parent

def log(msg):
    print(f'[VISION] {msg}')

# ═══════════════════════════════════════════
# 1. OCR — Scanned PDF → Text
# ═══════════════════════════════════════════

def ocr_pdf(pdf_path, lang='eng+ind', dpi=300):
    """Extract text from scanned PDF using OCR."""
    fp = Path(pdf_path)
    if not fp.exists():
        log(f'❌ File not found: {pdf_path}')
        return ''
    
    log(f'📄 OCR: {fp.name}')
    
    try:
        import fitz
        from PIL import Image
        import pytesseract
        import io
        
        doc = fitz.open(fp)
        text_pages = []
        
        for i, page in enumerate(doc):
            # First try extracting text directly
            text = page.get_text().strip()
            if len(text) > 50:
                log(f'  Page {i+1}: text layer found ({len(text)} chars)')
                text_pages.append(text)
                continue
            
            # No text layer — render as image and OCR
            log(f'  Page {i+1}: rendering for OCR...')
            pix = page.get_pixmap(dpi=dpi)
            img_data = pix.tobytes('png')
            img = Image.open(io.BytesIO(img_data))
            
            ocr_text = pytesseract.image_to_string(img, lang=lang)
            text_pages.append(f'[OCR Page {i+1}]\n{ocr_text}')
            
            log(f'  OCR complete: {len(ocr_text)} chars')
        
        doc.close()
        total_pages = len(text_pages)
        result = '\n\n'.join(text_pages)
        log(f'✅ OCR complete: {len(result)} total chars from {total_pages} pages')
        return result
    
    except ImportError as e:
        log(f'❌ Missing dependency: {e}')
        log('  Install: pip install pytesseract && apt-get install tesseract-ocr')
        return ''
    except Exception as e:
        log(f'❌ OCR failed: {e}')
        return ''

# ═══════════════════════════════════════════
# 2. IMAGE ANALYSIS
# ═══════════════════════════════════════════

def analyze_image(image_path, prompt="Describe this image in detail"):
    """Analyze an image using vision-capable model."""
    fp = Path(image_path)
    if not fp.exists():
        log(f'❌ File not found: {image_path}')
        return ''
    
    log(f'🖼️ Analyzing: {fp.name}')
    
    # Try to use GLM vision API
    try:
        import requests, base64
        
        with open(fp, 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
        
        # Try Sumopod vision endpoint
        resp = requests.post(
            'https://ai.sumopod.com/v1/chat/completions',
            headers={'Content-Type': 'application/json'},
            json={
                'model': 'glm-5.1',
                'messages': [
                    {
                        'role': 'user',
                        'content': [
                            {'type': 'text', 'text': prompt},
                            {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{img_b64}'}}
                        ]
                    }
                ],
                'temperature': 0.3,
                'max_tokens': 2048
            },
            timeout=30
        )
        
        if resp.status_code == 200:
            result = resp.json()['choices'][0]['message']['content']
            log(f'✅ Analysis complete ({len(result)} chars)')
            return result
        else:
            log(f'⚠️ Vision API returned {resp.status_code}, trying fallback...')
            return _analyze_image_fallback(fp, prompt)
    
    except Exception as e:
        log(f'⚠️ Vision API failed: {e}')
        return _analyze_image_fallback(fp, prompt)

def _analyze_image_fallback(fp, prompt):
    """Fallback: basic image info when vision API unavailable."""
    try:
        from PIL import Image
        img = Image.open(fp)
        w, h = img.size
        mode = img.mode
        fmt = img.format
        return f"Image info: {fmt} {w}x{h} {mode}. To analyze this image, use view_image tool."
    except Exception as e:
        return f'Could not process image: {e}'

# ═══════════════════════════════════════════
# 3. VIDEO PROCESSING
# ═══════════════════════════════════════════

def extract_frames(video_path, fps=1, output_dir=None, max_frames=20):
    """Extract frames from video using ffmpeg."""
    fp = Path(video_path)
    if not fp.exists():
        log(f'❌ File not found: {video_path}')
        return []
    
    if output_dir is None:
        now_str = datetime.now().strftime('%Y%m%d%H%M%S')
        output_dir = BASE / 'tmp' / f'frames_{now_str}'
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    log(f'🎬 Extracting frames from: {fp.name}')
    
    try:
        # Check video duration
        probe = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', str(fp)
        ], capture_output=True, text=True, timeout=10)
        
        duration = float(probe.stdout.strip()) if probe.stdout.strip() else 0
        log(f'  Duration: {duration:.1f}s')
        
        # Calculate frame interval
        total_frames = min(int(duration * fps), max_frames)
        interval = max(1, int(duration / total_frames))
        
        # Extract using ffmpeg
        output_pattern = str(Path(output_dir) / 'frame_%04d.png')
        result = subprocess.run([
            'ffmpeg', '-i', str(fp), '-vf', f'fps=1/{interval}',
            '-vframes', str(total_frames), '-y', output_pattern
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            log(f'⚠️ ffmpeg error: {result.stderr[:200]}')
            return []
        
        frames = sorted(Path(output_dir).glob('*.png'))
        log(f'✅ Extracted {len(frames)} frames to {output_dir}')
        return frames
    
    except FileNotFoundError:
        log('❌ ffmpeg not found. Install: apt-get install ffmpeg')
        return []
    except Exception as e:
        log(f'❌ Video processing failed: {e}')
        return []

def extract_subtitles(video_path):
    """Extract subtitles/audio transcript from video."""
    fp = Path(video_path)
    if not fp.exists():
        log(f'❌ File not found: {video_path}')
        return ''
    
    log(f'🎤 Extracting subtitles from: {fp.name}')
    
    try:
        # Try embedded subtitles first
        result = subprocess.run([
            'ffmpeg', '-i', str(fp), '-map', '0:s:0', '-f', 'srt', 'pipe:1'
        ], capture_output=True, text=True, timeout=30)
        
        if result.stdout:
            log(f'✅ Subtitles extracted ({len(result.stdout)} chars)')
            return result.stdout
        
        # No subtitles — try audio transcription note
        log('  No embedded subtitles found')
        return 'No subtitles available. Use YouTube API for auto-generated captions.'
    
    except Exception as e:
        log(f'❌ Subtitle extraction failed: {e}')
        return ''

# ═══════════════════════════════════════════
# 4. CHART ANALYSIS (specialized)
# ═══════════════════════════════════════════

def analyze_chart(chart_path):
    """Specialized stock chart analysis."""
    log('📈 Analyzing stock chart...')
    
    result = analyze_image(
        chart_path,
        prompt=(
            "Analyze this stock chart. Identify: 1) Trend direction (uptrend/downtrend/sideways), "
            "2) Key support/resistance levels, 3) Any chart patterns, 4) Volume analysis, "
            "5) Technical indicators if visible. Provide a brief market outlook."
        )
    )
    return result

# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Multi-modal vision engine')
    parser.add_argument('action', choices=['ocr', 'analyze', 'video', 'subtitles', 'chart'])
    parser.add_argument('path', help='File path')
    parser.add_argument('--prompt', default=None, help='Custom analysis prompt')
    parser.add_argument('--fps', type=float, default=1, help='Frames per second (video)')
    parser.add_argument('--output', default=None, help='Output directory')
    parser.add_argument('--lang', default='eng+ind', help='OCR language')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    if args.action == 'ocr':
        text = ocr_pdf(args.path, lang=args.lang)
        if args.format == 'json':
            print(json.dumps({'text': text, 'chars': len(text)}))
        else:
            print(text)
    
    elif args.action == 'analyze':
        prompt = args.prompt or "Describe this image in detail"
        result = analyze_image(args.path, prompt)
        print(result)
    
    elif args.action == 'video':
        frames = extract_frames(args.path, fps=args.fps, output_dir=args.output)
        print(f'Extracted {len(frames)} frames')
        for f in frames:
            print(f'  {f}')
    
    elif args.action == 'subtitles':
        subs = extract_subtitles(args.path)
        print(subs[:2000] if subs else 'No subtitles found')
    
    elif args.action == 'chart':
        result = analyze_chart(args.path)
        print(result)
