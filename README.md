# 🦊 Quill AI Assistant

> **AI Assistant yang bisa survive sendiri — bahkan kalau token API habis atau VPS mati.**

![Status](https://img.shields.io/badge/Status-L1-Full-Operation-brightgreen)
![Skills](https://img.shields.io/badge/Skills-27-Modules-blue)
![Survival](https://img.shields.io/badge/Survival-L1-red)

---

## 📊 System Status

| Metric | Value |
|--------|-------|
| **Level** | 🟢 L1 — Full Operation |
| **AI API** | OK |
| **Tools** | OK |
| **Disk** | 13% |
| **Skills** | 27 modules |
| **Chroma** | 2 entries |
| **Tests** | 8/8 PASSED |
| **Files** | 63 |
| **Updated** | 2026-05-03 10:59 UTC |

---

## 🎯 Quill Itu Apa?

AI assistant yang bisa:
- Beroperasi otomatis tanpa pengawasan
- Self-recovery kalau ada yang gagal
- Hemat resources (token, storage)
- Security assessment (authorized)
- Real-time monitoring (IDX disclosures)

---

## 🚀 Install

```bash
git clone https://github.com/Quillqueen11/Yolo.git
cd Yolo
pip install curl_cffi PyMuPDF
python3 survival/check_health.py
```

---

## 📁 Struktur

```
Yolo/
├── .bootstrap/      # Recovery system (MEMORY, SOUL, PROFILE backed up)
├── skills/          # 27 skill modules
├── scripts/         # Operational scripts
├── survival/        # Survival mode (L1/L3/L4)
└── docs/            # Documentation
```

---

## 🛡️ Survival Mode

Bertahan hidup mesmo kalau:

| Jika... | Quill switch ke... |
|---------|-------------------|
| API OK + tools OK | **L1** Full operation |
| API DOWN, tools OK | **L3** Local scripts only |
| Everything DOWN | **L4** Emergency shell only |

Auto-recovery setiap failure. No manual intervention needed.

---

## 🔧 Commands

```bash
# Health check
python3 survival/check_health.py

# Full system test
python3 survival/test_system.py

# Backup to GitHub
python3 .bootstrap/backup_state.py

# Restore (jika VPS mati)
python3 .bootstrap/restore.py
```

---

## 📊 Skills (27 Total)

security_expert | survival_mode | model_intelligence | chain_of_thought | context_compress | pdf_reader | reflex_boost | cron | browser_cdp | channel_message | docx | xlsx | news | himalaya | mythos_scaffold | natural_human_comm | make_plan | multi_agent_collaboration | chat_with_agent | QA_source_index | guidance | file_reader | pdf | pptx | browser_visible | dingtalk_channel | kimiim_deploy

---

## 🛡️ Security (OWASP Top 10)

Built-in payloads: SQLi bypass, NoSQLi, XSS, Command injection, JWT bypass, SSRF, XXE

---

## 🔄 Update

```bash
git pull origin main
```

---

**Maintainer:** quill.queen11@gmail.com

---

*Quill — AI yang bisa survive sendiri.* 🦊

_Updated: 2026-05-03 10:59 UTC_
