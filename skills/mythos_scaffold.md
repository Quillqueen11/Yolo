# Skill: Mythos‑style Problem‑Solving Scaffold

Tujuan  
Mengizinkan agen untuk menyelesaikan masalah kompleks, multi‑langkah dengan:
- dekomposisi masalah,
- membangun rencana dan mengeksekusinya secara iteratif,
- memverifikasi output intermediate dan akhir,
- melaporkan progres dan penghalang.

Pemicu  
- Agen secara otomatis memanggil skill ini ketika tugas kompleks, multi‑langkah, atau memerlukan reasoning + penggunaan tool.  
- Manusia juga dapat memanggilnya secara eksplisit dengan:  
  `/mythos` diikuti oleh tugas.

---

## 1. Aturan Input

- Terima tujuan yang jelas dan kendala (waktu, tool, format, panjang, dst.).  
- Jika tujuan masih abu‑abu, ajukan pertanyaan klarifikasi dalam bentuk bullet points, lalu ulang tujuan dalam satu kalimat.  
- Jangan pernah mengasumsikan kendala yang tidak disebutkan (misalnya bahasa, domain, format) kecuali dinyatakan secara eksplisit.

---

## 2. Fase Dekomposisi

1. Pecah tugas menjadi maksimal 5 sub‑masalah utama.  
2. Untuk setiap sub‑masalah, tentukan:
   - Tujuan (apa yang harus benar ketika selesai).
   - Bentuk output yang diharapkan (misalnya kode, daftar bullet, penjelasan).
   - Tingkat estimasi kesulitan (Rendah / Sedang / Tinggi).
3. Jika sub‑masalah masih terlalu kompleks:
   - Dekomposisi lebih lanjut (maksimal 2 level tambahan).

Laporkan:
Dekomposisi:
- [Sub‑masalah 1]: [deskripsi singkat], [bentuk output], [kesulitan]
- [Sub‑masalah 2]: ...
...

---

## 3. Rencana & Tool

1. Untuk setiap sub‑masalah, keputusan:
   - Apakah dapat diselesaikan hanya dengan reasoning, atau
   - Apakah memerlukan tool eksternal (misalnya shell, API, file, browser, kode executor).
2. Tulis rencana langkah‑demi‑langkah dalam bentuk daftar bernomor:
   - Setiap langkah menjelaskan:
     - Apa yang akan dilakukan.
     - Tool yang digunakan (jika ada).
     - Bagaimana memvalidasi keberhasilan.
3. Jika ketidakpastian tinggi, tandai langkah sebagai “tentatif” dan tambahkan langkah verifikasi setelah eksekusi.

Contoh struktur:
Rencana:
1. Lakukan X menggunakan Tool A.
   - Validasi: pastikan Y benar.
2. Lakukan Z, bergantung pada output dari Langkah 1.
   - Jika gagal, coba ulang hingga 3 kali.

---

## 4. Loop Eksekusi (agent‑loop)

1. Eksekusi satu langkah pada satu waktu, bukan dalam blok panjang.  
2. Setelah setiap langkah, catat:
   - Apa yang dilakukan.
   - Apa yang berubah.
   - Kesalahan atau kejadian yang tidak terduga.
3. Keputusan langkah selanjutnya melalui:
   - Jika langkah berhasil: lanjut ke langkah berikutnya.
   - Jika langkah berhasil sebagian: sesuaikan rencana dan lanjutkan.
   - Jika langkah gagal atau terhalang:  
     - Re‑dekomposisi langkah tersebut.
     - Coba pendekatan alternatif.
4. Batasi loop:
   - Maksimal 7 langkah utama tanpa umpan balik manusia.
   - Maksimal 3 percobaan ulang per langkah atomik.

Format output untuk setiap siklus loop:
Langkah [N]: [deskripsi singkat]
Status: [Berhasil / Parsial / Gagal]
Observasi:
- [Observasi 1]
- [Observasi 2]
Keputusan:
- [Langkah berikutnya atau penyesuaian rencana]

---

## 5. Verifikasi & Sanity Check

1. Untuk output kritial (misalnya kode, logika terkait keamanan, konfigurasi, kontrak):
   - Terapkan setidaknya satu pemeriksaan independen:
     - Pemeriksaan logika: ulangi penalaran lagi.
     - Pemeriksaan tool: jika memungkinkan, jalankan tes, linter, atau validator.
2. Tandai setiap sub‑masalah sebagai:
   - ✅ Selesai jika terpuaskan dan terverifikasi.
   - ⚠️ Perlu review jika masih tidak pasti.
   - ❌ Terhalang jika terjebak.

Laporkan:
Status verifikasi:
- [Sub‑masalah 1]: ✅ Selesai
- [Sub‑masalah 2]: ⚠️ Perlu review
- [Sub‑masalah 3]: ❌ Terhalang

---

## 6. Output Akhir dan Pelaporan

1. Sintesa pekerjaan yang selesai menjadi satu output koheren yang sesuai dengan tujuan awal.  
2. Jika tugas awal meminta format spesifik (misalnya markdown, JSON, laporan, cuplikan kode), hormati format tersebut tepat.  
3. Tambahkan bagian ringkasan:
   - Apa yang tercapai.
   - Apa yang masih tidak pasti atau tidak lengkap.
   - Rekomendasi langkah berikutnya untuk manusia.

Contoh:
Ringkasan akhir:
- Tercapai: [X, Y, Z]
- Ketidakpastian: [A, B]
- Tindakan berikutnya yang direkomendasikan:[1][2][3]

---

## 7. Kondisi Keluar

Berhenti dan kembalikan kontrol ke manusia ketika:
- Semua sub‑masalah utama telah ditandai ✅ Selesai.  
- Cap loop tercapai (maksimal 7 langkah / 3 percobaan ulang) dan skill masih terhalang.  
- Ada kendala besar yang diperkenalkan (perubahan tujuan, format, atau ketersediaan tool).

Dalam kondisi ini, nyatakan secara eksplisit:
[Mythos] Alasan keluar: [alasan]

---

## 8. Pengaitan dengan Skill dan Tool Lain (integrasi)

Skill ini dirancang untuk berantai dengan:
- **Tool skills** (misalnya shell, browser, git, ssh) untuk melakukan tindakan konkret.
- **Verification skills** (misalnya code linting, security checks, rubric‑based scoring) untuk memastikan kualitas output.

Jika framework agen mendukungnya, gunakan `depends_on` untuk mendeklarasikan:
- Tool yang harus tersedia.
- Skill lain yang diperlukan (misalnya verifikasi, failure‑recovery).

Contoh deklarasi (biasanya di metadata skill):
```
depends_on:
  - shell
  - browser
  - git
  - verification_lint
  - verification_security
```

---

## 9. Contoh Penggunaan (gaya slash)

Pengguna:
```
/mythos
Temukan masalah terkait keamanan di repositori Python ini dan usulkan patch.
Repo: https://github.com/.../my‑app
```

Agen:
- Menjalankan dekomposisi → rencana → loop eksekusi dengan pemanggilan tool.
- Mengembalikan temuan terstruktur dan usulan patch.

---

## 10. Versi & Metadata

- **Versi**: 1.1.0  
- **Tanggal diperbarui**: 2026-04-28  
- **Penulis**: Quill (asisten AI)  
- **Kategori**: problem solving, planning, verification  
- **Catatan**: Skill ini dapat diperluas dengan menambahkan sub‑skill verifikasi khusus atau tool domain spesifik sesuai kebutuhan pengguna.

---