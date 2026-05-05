# QUALITY GATE SKILL

## Purpose
Quality control system for automated news content.

---

## Quality Checks

### 1. Length Check

```python
def check_min_length(article, min_words=300):
    words = len(article.split())
    if words < min_words:
        return False, f"Too short: {words} words (min {min_words})"
    return True, f"OK: {words} words"
```

### 2. Structure Check

```python
def check_structure(article):
    """Ensure article has proper structure"""
    checks = []
    
    # Has title
    if article.count('\n') > 0:
        first_line = article.split('\n')[0]
        checks.append(len(first_line) > 10)
    
    # Has paragraphs (multiple line breaks)
    paragraphs = [p for p in article.split('\n\n') if p.strip()]
    checks.append(len(paragraphs) >= 3)
    
    # Has a conclusion/final section
    article_lower = article.lower()
    has_conclusion = any(word in article_lower for word in [
        'kesimpulan', 'kesimpulannya', 'menutup', 'akhirnya',
        'yang perlu dicermati', 'patut dipantau', 'menarik untuk'
    ])
    checks.append(has_conclusion)
    
    score = sum(checks) / len(checks) * 100
    return score >= 60, {"structure_score": score, "paragraphs": len(paragraphs)}
```

### 3. Fakta Check

```python
def verify_numbers(article):
    """Check that numbers referenced are accurate"""
    import re
    
    # Extract all numbers
    numbers = re.findall(r'Rp\s*[\d,.]+', article)
    percentages = re.findall(r'[\d,.]+%', article)
    dates = re.findall(r'\d+\s+(?:Mei|Juni|Juli|April|202\d)', article)
    
    # Basic sanity checks
    issues = []
    for num in numbers:
        val = num.replace('Rp', '').replace('.', '').replace(',', '').strip()
        try:
            if int(val) > 1000000000000000:  # More than 1 quadrillion
                issues.append(f"Suspiciously large: {num}")
        except:
            issues.append(f"Invalid number format: {num}")
    
    return len(issues) == 0, issues
```

### 4. Compliance Check

```python
def check_compliance(article):
    """Check against legal/safety requirements"""
    issues = []
    
    article_lower = article.lower()
    
    # Must have disclaimer for financial news
    must_have = ['disclaimer', 'bukan merupakan', 'rekomendasi', 'investasi']
    for term in must_have:
        if term not in article_lower:
            issues.append(f"Missing: '{term}'")
    
    # Must NOT have prohibited content
    prohibited = ['jaminan untung', 'pasti naik', 'dijamin cuan',
                   'tips rahasia', 'insider info']
    for term in prohibited:
        if term in article_lower:
            issues.append(f"Prohibited term: '{term}'")
    
    return len(issues) == 0, issues
```

### 5. Plagiarism / Duplicate Check

```python
def check_duplicate(article, existing_articles):
    """MinHash-based deduplication"""
    from hashlib import md5
    
    def shingles(text, k=10):
        """Generate shingles from text"""
        words = text.split()
        for i in range(len(words) - k + 1):
            yield ' '.join(words[i:i+k])
    
    def minhash(text):
        """Compute MinHash signature"""
        sig = set()
        for s in shingles(text):
            sig.add(md5(s.encode()).hexdigest()[:8])
        return sig
    
    article_sig = minhash(article)
    
    for existing in existing_articles:
        existing_sig = minhash(existing)
        jaccard = len(article_sig & existing_sig) / len(article_sig | existing_sig)
        if jaccard > 0.5:
            return False, f"Similarity: {jaccard:.0%}"
    
    return True, "Unique"
```

### 6. Tone Consistency Check

```python
def check_tone(article, target_tone="cnbc"):
    """Check tone consistency"""
    tone_signals = {
        "cnbc": {
            "positive": ['analis memperkirakan', 'konsensus', 'proyeksi',
                        'fundamental', 'katalis', 'data menunjukkan'],
            "negative": ['gejolak', 'volatilitas', 'tekanan', 'risiko']
        },
        "popular": {
            "positive": ['viral', 'ramai', 'trending', 'fenomena'],
            "negative": ['kontroversial', 'heboh', 'guncang']
        }
    }
    
    signals = tone_signals.get(target_tone, tone_signals["cnbc"])
    article_lower = article.lower()
    
    pos_count = sum(1 for s in signals["positive"] if s in article_lower)
    neg_count = sum(1 for s in signals["negative"] if s in article_lower)
    
    score = (pos_count - neg_count) / max(len(article.split()), 1) * 1000
    return score > -1, {"tone_score": score}
```

---

## Full Quality Gate

```python
def full_quality_gate(article, existing_articles=None):
    """Run all quality checks"""
    results = {
        "passed": True,
        "checks": [],
        "score": 100,
        "fixes_needed": []
    }
    
    checks = [
        ("length", check_min_length(article)),
        ("structure", check_structure(article)),
        ("numbers", verify_numbers(article)),
        ("compliance", check_compliance(article)),
        ("tone", check_tone(article)),
    ]
    
    if existing_articles:
        checks.append(("duplicate", check_duplicate(article, existing_articles)))
    
    for name, (passed, details) in checks:
        score = 100 if passed else 0
        results["checks"].append({
            "name": name,
            "passed": passed,
            "score": score,
            "details": details
        })
        if not passed:
            results["passed"] = False
            results["fixes_needed"].append(name)
        results["score"] = (results["score"] + score) / (len(checks) + 1) * (len(checks) + 1) - \
                          (100 - score if not passed else 0)
    
    results["score"] = max(0, min(100, results["score"]))
    return results
```

---

## Auto-Fix

```python
def auto_fix_article(article, qc_result):
    """Automatically fix quality issues"""
    
    fixed = article
    
    for check in qc_result["checks"]:
        if not check["passed"]:
            if check["name"] == "compliance":
                # Add disclaimer at end
                if "disclaimer" not in fixed.lower():
                    fixed += "\n\n---\n*Disclaimer: Artikel ini bersifat informatif dan bukan rekomendasi investasi.*"
            
            elif check["name"] == "structure":
                # Add concluding paragraph
                fixed += "\n\nKondisi ini tentunya menarik untuk terus dipantau ke depannya."
    
    return fixed
```

---

## Scoring System

```python
QUALITY_GRADES = {
    "A": (90, 100, "Siap publish"),
    "B": (75, 89, "Minor fixes needed"),
    "C": (50, 74, "Need revision"),
    "D": (0, 49, "Rewrite required")
}

def grade_article(score):
    for grade, (min_s, max_s, desc) in QUALITY_GRADES.items():
        if min_s <= score <= max_s:
            return grade, desc
    return "F", "Failed"
```

---

## Quick Test

```bash
python3 -c "
from skills.quality_gate import full_quality_gate, grade_article

article = '''Saham TLKM buyback Rp 1 triliun... (article text)'''
result = full_quality_gate(article)
grade, desc = grade_article(result['score'])
print(f'Grade: {grade} — {desc}')
print(f'Score: {result[\"score\"]}')
for c in result['checks']:
    print(f'  {c[\"name\"]}: {\"✅\" if c[\"passed\"] else \"❌\"} ({c[\"score\"]})')
"
```

---

_When to use: Before publishing any article to ensure quality, compliance, and uniqueness._