# Security Testing Skill — Super Expert Edition

## Deskripsi
Comprehensive web application & API security testing skill. Mengikuti OWASP Top 10 + API Security Testing methodology. Bisa mendeteksi dari vulnerability basic sampai advanced attack chains.

## Kemampuan
1. **Reconnaissance Super** — JS deep analysis, source map discovery, WebSocket detection, GraphQL introspection, subdomain enumeration, DNS zone transfer attempts, Shodan/Censys/Crt.sh integration
2. **OWASP Top 10** — Injection, Broken Auth, Sensitive Data Exposure, XXE, Broken Access Control, Security Misconfiguration, XSS, Insecure Deserialization, Known Vulnerabilities, Insufficient Logging
3. **API Security Testing** — REST/GraphQL/Soap/GQL endpoints, JWT analysis, OAuth 2.0 flows, IDOR enumeration, Mass Assignment, Rate Limit bypass, Pagination abuse
4. **Authentication/Authorization** — Session fixation, JWT algorithm confusion, OAuth redirect_uri bypass, MFA bypass, Password reset abuse, Privilege escalation
5. **Business Logic Testing** — Race conditions, workflow bypasses, pricing manipulation, integer overflow, parameter tampering
6. **Advanced Attacks** — SSRF, SSTI, XXE, Command Injection, Prototype Pollution, HTTP Request Smuggling, CRLF Injection
7. **Recon Tools** — Nuclei templates, SQLMap, ffuf, dirb, Amass, subfinder, waybackurls, gau

## Testing Phases

### Phase 1: Reconnaissance
```
- Subdomain enumeration (amass, subfinder, crt.sh)
- Port scanning (nmap patterns on known services)
- Technology fingerprinting (Wappalyzer patterns)
- JavaScript deep analysis (AST parsing, API extraction)
- Source map discovery (.map files)
- WebSocket detection
- GraphQL introspection
- Sitemap + robots.txt analysis
- GitHub/GitLab recon (github-search, gitrob)
- Shodan/Censys integration
```

### Phase 2: OWASP Top 10 Testing
```
A01 - Injection
  - SQLi (union, boolean, time-based, stacked)
  - NoSQLi (MongoDB, Redis operators)
  - Command Injection
  - LDAP Injection
  - XPath Injection
  - Template Injection (SSTI)
  - GraphQL Injection

A02 - Broken Authentication
  - JWT analysis (algorithm confusion, weak secret, none alg)
  - Session token predictability
  - Default credentials
  - Credential stuffing detection
  - OAuth 2.0 redirect_uri bypass
  - Password reset flaws
  - MFA bypass

A03 - Sensitive Data Exposure
  - Data at rest (backup files, .git, .env)
  - Data in transit (HTTP, cleartext creds)
  - Source code disclosure
  - Debug endpoints
  - Verbose errors / stack traces
  - Directory listing

A04 - XXE
  - XML external entity injection
  - File retrieval via XXE
  - SSRF via XXE
  - Billion laughs attack (DoS)

A05 - Broken Access Control
  - IDOR (parameter manipulation)
  - Vertical privilege escalation
  - Horizontal privilege escalation
  - Method tampering (GET→POST→DELETE)
  - API versioning bypass
  - Missing function level access control

A06 - Security Misconfiguration
  - Default credentials
  - Debug mode enabled
  - CORS misconfiguration
  - Directory listing
  - Unnecessary features
  - Missing security headers
  - Error page information disclosure

A07 - XSS
  - Reflected XSS
  - Stored XSS
  - DOM-based XSS
  - Mutation XSS
  - CSP bypass
  - Cookie stealing via XSS

A08 - Insecure Deserialization
  - Java deserialization
  - PHP unserialize abuse
  - Python pickle exploitation
  - YAML deserialization
  - JSON deserialization attacks

A09 - Known Vulnerabilities
  - CVE lookup (via API/Nuclei)
  - Outdated libraries (package.json, requirements.txt)
  - Writable /vendor or /node_modules
  - Exposed .git directory

A10 - Insufficient Logging
  - Missing audit trail
  - No rate limiting alerts
  - IP not logged
  - Failed login not logged
```

### Phase 3: Advanced API Testing
```
- GraphQL: introspection, batching, alias abuse, depth limit bypass
- REST: parameter fuzzing, method enumeration, version detection
- SOAP: WSDL analysis, XML injection
- JWT: alg:none attack, weak HMAC, kid injection, jku/x5u spoofing
- OAuth: redirect_uri, scope manipulation, token replay
- SSRF: DNS rebinding, open redirect chaining
- Race Conditions: parallel request timing attacks
- Mass Assignment: PUT/PATCH parameter overwriting
- HTTP Request Smuggling: CL.TE, TE.CL, TE.TE
```

### Phase 4: Exploitation (Authorized Only)
```
- Extract sensitive data from successful exploits
- Document attack chain from recon → exploit → data
- Generate PoC (not destructive)
- Assess real-world impact
```

## Output Format
```
## [CRITICAL/HIGH/MEDIUM/LOW/INFO] Title
- Endpoint: URL
- Method: GET/POST/etc
- Parameter: vulnerable param
- Payload: actual exploit string
- Response: what was returned
- Impact: real-world consequence
- PoC: curl command or request
- Remediation: recommended fix
```

## Catatan
- Only test systems with authorization
- Never destructive — document, don't destroy
- Report financial exploitation attempts immediately
- Focus on real-world impact, not theoretical CVSS scores