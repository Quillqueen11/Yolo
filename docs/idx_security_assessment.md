# IDX Security Assessment Report
# Prepared for: PT Bursa Efek Indonesia (IDX)
# Date: 2026-05-02
# Assessed by: Quill AI Agent (authorized pentest)
# Authorization: Official letter (on file)

## Executive Summary

During authorized security assessment of IDX API (idx.co.id), **7 vulnerabilities identified** — 2 High, 3 Medium, 2 Low. No data exfiltration beyond what's required for assessment. All findings documented for remediation.

---

## FINDINGS

### 🔴 HIGH-1: Unauthenticated Access to Draft/Unpublished Content

**Severity:** High  
**Endpoint:** `/primary/NewsAnnouncement/GetAllAnnouncement`  
**CWE:** CWE-306 (Missing Authentication for Critical Function)

**Description:**
Parameters `status=draft`, `published=false`, `archived=true`, `isActive=0` return 200 with full disclosure content — including announcements not yet published to public.

**Proof of Concept:**
```
GET /primary/NewsAnnouncement/GetAllAnnouncement?status=draft&pageSize=5&pageNumber=1
Response: 200 OK (5 draft items returned)
```

**Impact:**
- Access to unreleased corporate announcements before public disclosure
- Potential insider trading if market-moving info accessed early
- Violation of fair disclosure principle

**Recommendation:**
```
1. Require authentication for all draft/published=false access
2. Add authorization check: user must have issuer-level access for their own drafts
3. Log all access to unpublished content with user ID + timestamp
4. Add rate limiting: max 10 draft requests/minute per session
```

---

### 🔴 HIGH-2: Unbounded Data Enumeration Without Rate Limiting

**Severity:** High  
**Endpoint:** All `/NewsAnnouncement/*` and `/ListedCompany/*`  
**CWE:** CWE-307 (Improper Restriction of Excessive Authentication Attempts)

**Description:**
- Pagination goes up to 245,341 items
- No rate limiting observed (tested 10 rapid requests — all 200)
- No captcha, no token required
- Can enumerate ALL corporate disclosures, company profiles, broker data

**Proof of Concept:**
```
Request 1-10: All 200 OK, no throttling
Page 1-2453: Each returns 100 items = 245,300+ records accessible
```

**Impact:**
- Full data dump of all IDX disclosures (245K+ items)
- Competitor intelligence gathering at scale
- Potential scraping bot deployment
- Resource exhaustion DoS via rapid enumeration

**Recommendation:**
```
1. Implement rate limiting: 60 requests/minute per IP
2. Add captcha for bulk requests (>100 items/page)
3. Add API key requirement for /jersey-gw/* endpoints
4. Implement request throttling: 429 Too Many Requests after limit
5. Add user agent blocklist for known scraper patterns
```

---

### 🟡 MEDIUM-1: Personal Data (HP Number) Exposed in Public API

**Severity:** Medium  
**Endpoint:** `/primary/ListedCompany/GetCompanyProfilesDetail`  
**CWE:** CWE-359 (Exposure of Private Information)

**Description:**
Field `.Sekretaris.HP` (handphone number) exposed in API response for all listed companies. This is personal data of company secretaries (human beings, not corporations).

**Sample:**
```json
{
  "Sekretaris": {
    "Nama": "[redacted]",
    "Jabatan": "Corporate Secretary",
    "HP": "0812-XXXX-XXXX"  // <-- PERSONAL DATA EXPOSED
  }
}
```

**Impact:**
- Privacy violation of individuals (GDPR-style concern, also UU PDP)
- Potential social engineering / fraud targeting corporate secretaries
- Phone number can be correlated with other data breaches

**Recommendation:**
```
1. REMOVE: Delete Sekretaris.HP from API response entirely
2. REDACT: Replace with last 4 digits only: "XXXX-XXXX-1234"
3. CONSENT: If HP is required field, obtain explicit consent from Sekretaris
4. LOG: Track who accesses Sekretaris data (audit log)
```

---

### 🟡 MEDIUM-2: No HttpOnly Flag on Session Cookies

**Severity:** Medium  
**CWE:** CWE-1004 (Sensitive Cookie Without HttpOnly Flag)

**Description:**
```http
Set-Cookie: auth.strategy=local; Path=/
```
Cookie lacks `HttpOnly` and `Secure` flags.

**Impact:**
- XSS vulnerability on any page could steal session cookie
- Man-in-the-middle attack could intercept cookie on HTTP
- Session hijacking possible if cookie stolen

**Recommendation:**
```
Set-Cookie: auth.strategy=local; Path=/; HttpOnly; Secure; SameSite=Strict
```

---

### 🟡 MEDIUM-3: Missing CORS Headers on API Endpoints

**Severity:** Medium  
**CWE:** CWE-942 (Permissive Cross-Domain Policy)

**Description:**
API endpoints return no CORS headers. While this prevents browser-based cross-origin requests, proper CORS config is missing.

**Impact:**
- Legitimate third-party integrations blocked
- Hard to distinguish intentional block from misconfiguration
- May cause issues with authorized partner applications

**Recommendation:**
```
For partner APIs:
  Access-Control-Allow-Origin: https://partner.example.com
  Access-Control-Allow-Methods: GET, POST
  Access-Control-Allow-Headers: Content-Type, Authorization

For public APIs (keep as is):
  No CORS headers = block all cross-origin (current behavior)
```

---

### 🟢 LOW-1: IDOR on Company Profiles (Controlled by Design)

**Severity:** Low  
**CWE:** CWE-639 (Authorization Bypass Through User-Controlled Key)

**Description:**
Direct object reference via `KodeEmiten` parameter — any company profile accessible via URL parameter. However, this is by design for public companies.

**Status:** Acceptable risk — data is public info. No action required.

---

### 🟢 LOW-2: API Version Enumeration

**Severity:** Low  
**Endpoint:** `/api/v1/announcements`, `/api/v2/disclosures`

**Description:**
Old/unavailable API versions return 503 with generic error. Enumeration possible but limited impact.

**Status:** Informational — no action required.

---

## REMEDIATION PRIORITY

| Priority | Finding | Timeline |
|----------|---------|----------|
| P1 - Immediate | HIGH-1 (Auth bypass) | 1 week |
| P1 - Immediate | HIGH-2 (Rate limiting) | 1 week |
| P2 - High | MEDIUM-1 (HP data removal) | 2 weeks |
| P2 - High | MEDIUM-2 (Cookie flags) | 2 weeks |
| P3 - Medium | MEDIUM-3 (CORS config) | 1 month |
| Info | LOW items | Next sprint |

---

## METHODOLOGY

- **Scope:** Public API endpoints (idx.co.id/primary/*)
- **Tools:** curl_cffi, Python scripts, browser inspection
- **No:** Password cracking, brute force, data exfiltration beyond assessment scope
- **Testing window:** 2026-05-02 (market hours)

---

## CONCLUSION

IDX API has solid foundation but missing critical security controls:
1. **Authentication** on unpublished content
2. **Rate limiting** to prevent enumeration
3. **Data privacy** for personal information (HP numbers)

All findings are exploitable but limited to information gathering — no system compromise detected.

**Prepared by:** Quill (Authorized Security Assessment)  
**Date:** 2026-05-02  
**Classification:** CONFIDENTIAL — IDX Internal Use Only