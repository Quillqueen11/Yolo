# Skill: kimiim‑cli deploy

Tujuan
Mudahkan penggunaan `kimiim-cli` untuk mendeploy aplikasi atau layanan ke target yang didukung (misalnya cloud, server, atau platform khusus). Skill ini menyediakan langkah demi langkah untuk memeriksa persyaratan, menjalankan perintah deploy, dan memverifikasi hasil.

Pemicu
- Otomatis dipanggil ketika pengguna menyatakan keinginan mendeploy sesuatu menggunakan kimiim-cli (misalnya “deploy aplikasi saya dengan kimiim-cli”).
- Juga dapat dipanggil secara eksplisit dengan perintah: `/kimiim-deploy [parameter]`.

---

## 1. Input rules

Terima deskripsi singkat tentang apa yang ingin dideploy dan opsional:
- Path ke kode atau artefak (misalnya `./app`, `build/`).
- Lingkungan target (misalnya `staging`, `production`).
- Konfigurasi khusus (misalnya flag `--flag`, variabel lingkungan).
Jika input tidak lengkap, ajukan pertanyaan klarifikasi dalam bentuk bullet points, lalu ringkas permintaan dalam satu kalimat sebelum melanjutkan.

---

## 2. Persyaratan & persiapan

1. Pastikan `kimiim-cli` terinstal dan berada di PATH.
   - Cek dengan menjalankan `kimiim-cli --version`.
2. Jika diperlukan autentikasi (misalnya token, API key), pastikan sudah diset dalam variabel lingkungan atau file konfigurasi yang sesuai dengan dokumentasi kimiim-cli.
3. Pastikan direktori kerja berisi artefak yang akan dideploy (jika diperlukan).

Jika persyaratan tidak terpenuhi, beri instruksi singkat untuk menginstall atau mengkonfigurasi kimiim-cli, lalu hentikan skill sampai pengguna menyiapkannya.

---

## 3. Rencana langkah demi langkah

Berikut contoh rencana umum (akan disesuaikan berdasarkan input pengguna):

1. **Validasi input**
   - Tool: reasoning saja.
   - Validasi: path ada, target environment dikenali.

2. **Persiapan artefak (jika diperlukan)**
   - Tool: shell (misalnya `npm run build`, `make`, atau copy file).
   - Validasi: artefak berhasil dibuat atau tersedia.

3. **Menjalankan perintah deploy kimiim-cli**
   - Tool: shell dengan perintah seperti:
     ```
     kimiim-cli deploy --path <path> --env <env> [flags lain]
     ```
   - Validasi: perintah selesai dengan kode exit 0 dan output yang mengindikasikan sukses.

4. **Verifikasi hasil deploy**
   - Tool: tergantung target (misalnya curl ke endpoint, cek logs, atau perintah `kimiim-cli status`).
   - Validasi: layanan merespon sesuai ekspektasi.

5. **Laporkan hasil**
   - Beri ringkasan singkat: sukses, URL atau informasi akses, dan catatan bila ada peringatan.

Jika ketidakpastian tinggi pada suatu langkah, tandai sebagai “tentatif” dan tambahkan langkah verifikasi setelahnya.

---

## 4. Eksekusi loop (agent‑loop)

1. Jalankan satu langkah pada satu waktu.
2. Setelah setiap langkah, catat:
   - Apa yang dilakukan.
   - Apa yang berubah.
   - Error atau kejadian tidak terduga.
3. Keputusan lanjut:
   - Jika langkah berhasil → lanjut ke langkah berikutnya.
   - Jika langkah berhasil sebagian → sesuaikan rencana dan lanjutkan.
   - Jika langkah gagal atau terhalang →
     - Re‑dekomposisi langkah tersebut.
     - Coba pendekatan alternatif (misalnya perintah lain, flag berbeda).
4. Batas:
   - Maksimal 7 langkah utama tanpa umpan balik manusia.
   - Maksimal 3 percobaan ulang per langkah atomik.

Format output tiap siklus:
Langkah [N]: [deskripsi singkat]
Status: [Berhasil / Parsial / Gagal]
Observasi:
- [Observasi 1]
- [Observasi 2]
Keputusan:
- [Langkah berikutnya atau penyesuaian rencana]

---

## 5. Verifikasi & sanity check

- Setelah deploy selesai, lakukan minimal satu verifikasi independen:
  - Jika layanan web: buka URL atau jalankan `curl -f <url>` dan pastikan kode HTTP 2xx.
  - Jika layanan backend: periksa logs atau jalankan perintah status kimiim-cli.
  - Jika infrastruktur: gunakan perintah cli lain untuk melihat resource yang dibuat.
- Jika verifikasi gagal, catat sebagai ⚠️ Needs review atau ❌ Blocked sesuai situasi.

Laporkan status tiap sub‑masalah:
- ✅ Selesai
- ⚠️ Perlu review
- ❌ Terhalang

---

## 6. Output akhir dan pelaporan

- Sajikan hasil deploy dalam bentuk yang jelas dan singkat.
- Jika pengguna meminta format tertentu (misalnya JSON, markdown), ikuti format itu.
- Tambahkan bagian ringkasan:
  - Apa yang berhasil dideploy.
  - Informasi akses (URL, endpoint, dsb.).
  - Apa yang masih tidak pasti atau perlu dilakukan manual.
  - Rekomendasi langkah berikutnya untuk pengguna.

Contoh ringkasan:
- Tercapai: Aplikasi berhasil dideploy ke staging di https://staging.example.com
- Ketidakpastian: Perlu mengatur variabel lingkungan `API_KEY` secara manual.
- Tindakan berikutnya: Set variabel lingkungan lalu jalankan `kimiim-cli restart`.

---

## 7. Kondisi keluar

Berhenti dan kembalikan kontrol ke manusia ketika:
- Semua sub‑masalah utama berstatus ✅ Selesai.
- Mencapai batas loop (7 langkah/3 ulang) dan masih terhalang.
- Ada kendala besar yang di‑input ulang (ubah target, format, atau ketersediaan tool).

Nyatakan secara eksplisit:
[kimiim-deploy] Alasan keluar: [alasan]

---

## 8. Contoh penggunaan

Pengguna:
```
/kimiim-deploy
Deploy aplikasi Node.js saya ke staging dengan kimiim-cli.
Path: ./app
Env: staging
Flag: --token=$KIMIIM_TOKEN
```

Agen:
- Mengecek kimiaim-cli terinstal.
- Membangun (jika perlu) dengan `npm install --prefix ./app && npm run build --prefix ./app`.
- Menjalankan: `kimiim-cli deploy --path ./app/build --env staging --token=$KIMIIM_TOKEN`.
- Memverifikasi dengan curl ke URL yang diberikan oleh kimiim-cli.
- Mengembalikan ringkasan hasil.

---

## 9. Versi & metadata

- Versi: 1.0.0
- Tanggal: 2026-04-28
- Kategori: deployment, cli, kimiim