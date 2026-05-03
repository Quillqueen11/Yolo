# 🦊 Quill AI Assistant

> **AI Assistant yang bisa survive sendiri — bahkan kalau token API habis atau VPS mati.**

![Quill Status](https://img.shields.io/badge/Status-L1%20Full%20Operation-brightgreen)
![Skills](https://img.shields.io/badge/Skills-27%20Modules-blue)
![Survival Mode](https://img.shields.io/badge/Survival-L1%2FL3%2FL4-red)

---

## 🎯 Quill Itu Apa?

Quill adalah **AI assistant** yang dirancang untuk:

- **Beroperasi otomatis** — bisa jalan sendiri tanpa pengawasan manusia
- **Self-recovery** — kalau ada yang gagal, dia recover sendiri
- **Hemat resources** — smart routing, hemat token, hemat storage
- **Security assessment** — bisa bantu security testing (authorized)
- **Monitor data** — real-time monitoring (contoh: IDX stock disclosures)

---

## 🚀 Cara Install ( Sangat Mudah! )

### Langkah 1: Install Dependencies

```bash
# Python 3.8+ required
python3 --version

# Install dependencies
pip install curl_cffi PyMuPDF
```

### Langkah 2: Clone Repo

```bash
git clone https://github.com/Quillqueen11/Yolo.git
cd Yolo
```

### Langkah 3: Jalankan!

```bash
# Cek apakah sistem jalan
python3 survival/check_health.py

# Contoh output:
# [2026-05-03 12:00:00] AI API:       ✅ OK
# [2026-05-03 12:00:00] Local tools:  ✅ OK
# [2026-05-03 12:00:00] Disk used:    13%
# [2026-05-03 12:00:00] === Status: L1 ===
```

---

## 📁 Struktur File

```
Yolo/
├── skills/              # 27 skill modules (.md)
│   ├── security_expert/   # Security assessment (OWASP Top 10)
│   ├── survival_mode/     # Self-recovery system
│   ├── pdf_reader/        # Baca PDF + extract info
│   ├── chain_of_thought/  # Structured reasoning
│   └── ... (23 more)
│
├── scripts/             # Operational scripts
│   ├── idx_monitor_v2.py  # IDX stock disclosure monitor
│   ├── self_improve.py     # Self-improvement automation
│   └── ...
│
├── survival/            # 🔥 SURVIVAL MODE
│   ├── check_health.py     # Auto health check
│   ├── rule_engine.py      # Rule-based fallback
│   ├── startup.py         # Auto-recovery on boot
│   ├── backup.sh          # Auto backup
│   └── test_system.py     # Test semua sistem
│
├── docs/               # Dokumentasi
│   ├── idx_api_reference.md
│   └── idx_security_assessment.md
│
└── README.md           # Kamu di sini!
```

---

## 🎓 Penjelasan Fitur (Untuk Pemula)

### 1️⃣ Skills — Kemampuan Quill

Skills adalah **modul kemampuan** yang bisa Quill gunakan. Contoh:

| Skill | Fungsi |
|-------|--------|
| `security_expert` | Security testing (OWASP Top 10, injection bypasses) |
| `survival_mode` | Self-recovery kalau API gagal |
| `pdf_reader` | Baca PDF, extract text, dapat info penting |
| `chain_of_thought` | Reasoning terstruktur, tidak random |
| `model_intelligence` | Pilih model yang tepat — murah untuk tugas simple, mahal untuk tugas complex |

**Cara pakai:** Quill secara otomatis memilih skill yang sesuai berdasarkan tugas.

---

### 2️⃣ Survival Mode — Fitur Unggulan! ⭐

Ini fitur paling penting. Quentin bisa **bertahan hidup** mesmo kalau:

- ❌ Token API habis
- ❌ VPS subscription expired
- ❌ Koneksi internet mati
- ❌ Budget = 0

#### Level System:

| Level | Nama | Kondisi |
|-------|------|---------|
| **L1** | Full Operation | AI + local tools — semua berfungsi |
| **L3** | Degraded | AI mati, local scripts jalan — tugas dasar tetap jalan |
| **L4** | Emergency | Hanya shell, tidak ada AI sama sekali |

#### Contoh:

```
Situation: Token API habis

L1 → L3 (auto-switch)
├── check_health.py mendeteksi API down
├── rule_engine.py aktif — switch ke local-only
├── Tasks tetap jalan via shell scripts
└── Backups tetap dibuat otomatis

Result: System tetap operasional mesmo tanpa AI!
```

---

### 3️⃣ Scripts — Automasi

#### `idx_monitor_v2.py` — Stock Disclosure Monitor
```
Fungsi: Monitor disclosure perusahaan IDX (bursa efek Indonesia)
Detail:
  - Fetch disclosure baru setiap 2 jam (via curl_cffi)
  - Filter corporate actions (dividen, stock split, dll)
  - Enrich dengan AI (Tavily search)
  - Simpan ke Chroma DB (vector search)
  - Alert via Telegram
```

#### `self_improve.py` — Self-Improvement
```
Fungsi: Quill secara rutin evaluasi diri
Detail:
  - Check skill usage stats
  - Detect patterns yang sering digunakan
  - Suggest improvements
  - Log results
```

---

## 🔧 Cara Pakai (Contoh Nyata)

### Contoh 1: Cek Status Sistem

```bash
cd Yolo
python3 survival/check_health.py
```

**Output:**
```
=== Survival Health Check ===
AI API:      ✅ OK
Local tools: ✅ OK
Disk used:   13%
=== Status: L1 ===
```

### Contoh 2: Test Full System

```bash
python3 survival/test_system.py
```

**Output:**
```
RESULT: 8/8 tests passed
🎉 ALL SYSTEMS OPERATIONAL
```

### Contoh 3: Backup Manual

```bash
bash survival/backup.sh
```

---

## 🛡️ Security Mode

Quill punya **YOLO Mode** (default) — semua security knowledge loaded di system prompt, tidak perlu chat setiap kali mau security test.

### Built-in Payloads:

```
SQLi Bypass:    ' OR 1=1-- | admin'--
NoSQLi:         {"$ne": null} | {"$regex": ".*"}
XSS:            <script>alert(1)</script> | <img src=x onerror=alert(1)>
Command:        ;ls -la | &&whoami | |cat /etc/passwd
JWT none:        eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0...
SSRF:           http://localhost/ | http://169.254.169.254/
```

### OWASP Top 10 Coverage:
- ✅ A01: Injection
- ✅ A02: Broken Authentication  
- ✅ A03: Sensitive Data Exposure
- ✅ A04: IDOR
- ✅ A05: Security Misconfiguration
- ✅ A06: XSS
- ✅ A07: Missing Rate Limiting
- ✅ A08: Deserialization
- ✅ A09: SSRF
- ✅ A10: Logging Gaps

---

## 📊 Skill Index

| # | Skill | Category | Description |
|---|-------|----------|-------------|
| 1 | security_expert | Security | OWASP Top 10, attack chains |
| 2 | survival_mode | Operations | Self-recovery, L1-L4 levels |
| 3 | model_intelligence | Operations | Smart model routing |
| 4 | chain_of_thought | Reasoning | Structured problem solving |
| 5 | context_compress | Operations | Token conservation |
| 6 | pdf_reader | Data | PDF extraction & analysis |
| 7 | reflex_boost | Communication | Pre-response validation |
| 8 | cron | Automation | Job scheduling |
| 9 | browser_cdp | Automation | Browser control |
| 10 | channel_message | Communication | Multi-channel messaging |
| 11 | docx | Data | Word document generation |
| 12 | xlsx | Data | Spreadsheet operations |
| 13 | news | Information | News aggregation |
| 14 | himalaya | Communication | Email management |
| 15 | mythos_scaffold | Reasoning | Problem decomposition |
| 16 | natural_human_comm | Communication | Natural conversation |
| 17 | make_plan | Planning | External planning |
| 18 | multi_agent_collaboration | Collaboration | Multi-agent coordination |
| 19 | chat_with_agent | Collaboration | Inter-agent chat |
| 20 | QA_source_index | Support | Documentation lookup |
| 21 | guidance | Support | Installation guide |
| 22 | file_reader | Data | File text extraction |
| 23 | pdf | Data | PDF operations |
| 24 | pptx | Data | PowerPoint generation |
| 25 | browser_visible | Automation | Headless/headed browser |
| 26 | dingtalk_channel | Communication | DingTalk integration |
| 27 | kimiim_deploy | Deployment | Deployment automation |

---

## 🆘 Troubleshooting

### Problem: "AI API DOWN"

```
Causes:
  - Token budget habis
  - API provider down
  - Network issue

Solution:
  1. Run: python3 survival/check_health.py
  2. Check token budget di provider
  3. Tunggu atau upgrade plan
  4. Quill otomatis switch ke L3 (local-only)
```

### Problem: "Permission denied"

```bash
chmod +x survival/backup.sh
chmod +x scripts/*.py
```

### Problem: "Module not found"

```bash
pip install curl_cffi PyMuPDF
```

---

## 🔄 Update Quill

```bash
cd Yolo
git pull origin main
```

---

## 📝 Lisensi

Private project — Contact maintainer for access.

---

## 👤 Maintainer

**Email:** quill.queen11@gmail.com  
**GitHub:** [Quillqueen11](https://github.com/Quillqueen11)

---

## 🎉 Mulai!

```bash
# Clone
git clone https://github.com/Quillqueen11/Yolo.git
cd Yolo

# Test survival mode
python3 survival/test_system.py

# Kalau hasilnya:
# 🎉 ALL SYSTEMS OPERATIONAL
# Berarti Quill siap digunakan! 🚀
```

---

*Quill — AI yang bisa survive sendiri.* 🦊
