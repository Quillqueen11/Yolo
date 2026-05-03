# ===========================================
# 🦊 QUILL BOOTSTRAP — Full Recovery Guide
# ===========================================

> **Bagaimana restore Quill 100% dari GitHub kalau VPS hilang atau perlu deploy di server baru.**

---

## Apa Itu Bootstrap?

Bootstrap adalah sistem **auto-restore** yang bikin Quill bisa di-deploy ulang 100% dari GitHub. Including:

- ✅ Identity (siapa Quill, siapa Andry)
- ✅ Memory (riwayat percakapan, keputusan)
- ✅ Core files (SOUL.md, PROFILE.md, MEMORY.md)
- ✅ Config template (API keys)
- ✅ State files (IDX monitor state, survival state)

---

## Sebelum VPS Mati (Backup)

```bash
cd /app/working/workspaces/default/github/quill

# Jalankan backup script
python3 .bootstrap/backup_state.py

# Output:
# [BOOTSTRAP] === Quill State Backup ===
# [BOOTSTRAP] ✅ MEMORY.md
# [BOOTSTRAP] ✅ PROFILE.md
# [BOOTSTRAP] ✅ SOUL.md
# [BOOTSTRAP] Backed up 6/6 files
# [BOOTSTRAP] 🎉 State backup complete!
```

Script ini otomatis commit + push ke GitHub kalau credentials tersedia.

---

## Sesudah VPS Mati (Restore)

### Opsi 1: Auto-Restore (Recommended)

```bash
# Clone repo
git clone https://github.com/Quillqueen11/Yolo.git
cd Yolo

# Jalankan auto-restore
python3 .bootstrap/restore.py
```

**Output:**
```
==================================================
  🦊 QUILL AUTO-RESTORE
==================================================

 Step 1: Checking Prerequisites
 ✅ Python3: Python 3.11.2
 ✅ Git: git version 2.39.5

 Step 2: Restoring from GitHub
 ✅ Repo already cloned
 ✅ Pulled latest changes

 Step 3: Restoring Identity Files
 ✅ MEMORY.md
 ✅ SOUL.md
 ✅ PROFILE.md

 Step 4: Setting Up Directories
 ✅ /app/working/workspaces/default/data
 ✅ /app/working/workspaces/default/survival/backup
 ...

 Step 5: Checking Dependencies
 ✅ curl_cffi
 ✅ PyMuPDF

 Step 6: Running System Test
 RESULT: 8/8 tests passed
 🎉 ALL SYSTEMS OPERATIONAL

==================================================
  🎉 RESTORE COMPLETE!
  Quill is ready for operation! 🚀
==================================================
```

---

### Opsi 2: Manual Restore

```bash
# 1. Copy identity files
cp .bootstrap/MEMORY.md ../MEMORY.md
cp .bootstrap/SOUL.md ../SOUL.md
cp .bootstrap/PROFILE.md ../PROFILE.md

# 2. Setup config
cp .bootstrap/config.env.example ../.env
nano ../.env  # Edit dengan API keys kamu

# 3. Create directories
mkdir -p ../data ../survival/backup ../survival/logs

# 4. Test
python3 survival/test_system.py
```

---

## File Bootstrap

```
.bootstrap/
├── MEMORY.md              ← Long-term memory (backup before VPS die)
├── SOUL.md                ← Core identity
├── PROFILE.md             ← User profile
├── config.env.example     ← Config template (fill API keys)
├── bootstrap.sh           ← Shell script (legacy)
├── backup_state.py       ← Auto-backup to GitHub
└── restore.py            ← Auto-restore from GitHub
```

---

## Config Setup (.env)

```bash
# Copy template
cp .bootstrap/config.env.example .env

# Edit dengan API keys kamu
nano .env

# Isi yang diperlukan:
# - SUMOPOD_API_KEY
# - TAVILY_API_KEY
# - TELEGRAM_BOT_TOKEN
```

**Template:**
```env
# Primary AI API
SUMOPOD_API_KEY=your_key_here
SUMOPOD_BASE_URL=https://ai.sumopod.com

# Web Search
TAVILY_API_KEY=tvly-dev-your_key_here

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
USER_CHAT_ID=924535843
USER_NAME=Andry
```

---

## Cron untuk Auto-Backup

Tambahkan ke crontab untuk auto-backup setiap jam:

```bash
# Edit crontab
crontab -e

# Tambah line:
0 * * * * cd /app/working/workspaces/default/github/quill && python3 .bootstrap/backup_state.py >> /var/log/quill_backup.log 2>&1
```

---

## Troubleshooting

### "bootstrap.sh not found"

```bash
# Pastikan kamu di direktori Yolo
cd Yolo
ls -la .bootstrap/
```

### "Permission denied"

```bash
chmod +x .bootstrap/bootstrap.sh
chmod +x .bootstrap/backup_state.py
chmod +x .bootstrap/restore.py
```

### "Module not found"

```bash
pip install curl_cffi PyMuPDF chromadb
```

### "restore.py failed"

Cek apakah repo sudah benar di-clone:

```bash
ls -la .bootstrap/MEMORY.md
# Should exist
```

---

## Summary

| Action | Command |
|--------|---------|
| Backup (before VPS die) | `python3 .bootstrap/backup_state.py` |
| Auto-restore (new VPS) | `python3 .bootstrap/restore.py` |
| Manual restore | Copy files manually |
| Test system | `python3 survival/test_system.py` |

---

## Level System After Restore

Setelah restore, Quill akan berada di level sesuai kondisi:

| Level | Kondisi | Kemampuan |
|-------|---------|-----------|
| **L1** | API OK + tools OK | Full operation |
| **L3** | API DOWN, tools OK | Local scripts only |
| **L4** | API DOWN, tools minimal | Emergency mode |

---

*Bootstrap ensures Quill never truly dies — clone from GitHub, restore, and he's back.* 🦊
