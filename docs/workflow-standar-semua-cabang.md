# Standar Workflow Operasional Semua Cabang (Rumba)

Dokumen ini mendefinisikan alur kerja baku agar seluruh cabang menjalankan proses dengan cara yang sama, terukur, dan bisa diaudit.

Referensi role mengikuti dokumen: `docs/erpnext-role-permission-matrix.md`.

## 1) Prinsip Standardisasi

1. Satu nama status untuk semua cabang (tidak boleh alias lokal).
2. Satu titik approval per tahapan kritikal.
3. Semua perubahan pasca-submit wajib jejak audit (`Cancel + Amend`, bukan edit bebas).
4. SLA (Service Level Agreement) per tahap wajib dipantau mingguan.
5. Exception hanya boleh dengan alasan tertulis dan approval `Rumba Admin Utama`.

## 2) Workflow Inti per Proses

## 2.1 Pendaftaran Murid

Urutan status:
1. `Draft`
2. `Data Verification`
3. `Placement Review`
4. `Ready to Invoice`
5. `Enrolled`
6. `Cancelled`

Aturan:
1. `Rumba Admin Unit` membuat pendaftaran di `Draft`.
2. Validasi dokumen di `Data Verification` wajib cek identitas, unit, program, dan kontak orang tua.
3. Penentuan kelas di `Placement Review` wajib isi kelas awal, tutor, dan jadwal.
4. `Ready to Invoice` hanya jika data lengkap 100%.
5. `Enrolled` hanya jika invoice terbit dan kebijakan pembayaran awal terpenuhi.
6. Jika batal, gunakan `Cancelled` dengan alasan wajib.

SLA:
1. `Draft -> Ready to Invoice`: maksimal 1 hari kerja.
2. `Ready to Invoice -> Enrolled`: maksimal 1 hari kerja setelah pembayaran valid.

## 2.2 Operasional Kelas & Kehadiran

Urutan status sesi kelas:
1. `Scheduled`
2. `In Progress`
3. `Attendance Submitted`
4. `Attendance Approved`
5. `Needs Correction`

Aturan:
1. `Rumba Tutor` mengisi presensi paling lambat H+0 setelah kelas selesai.
2. `Rumba Admin Unit` memverifikasi presensi (jam, jumlah hadir, catatan khusus).
3. Jika ada mismatch, pindahkan ke `Needs Correction` lalu balik ke tutor.
4. Presensi final hanya `Attendance Approved`.

SLA:
1. Input presensi: maksimal 6 jam setelah kelas selesai.
2. Approval presensi: maksimal H+1.

## 2.3 Keuangan (Invoice & Payment)

Urutan status invoice:
1. `Draft`
2. `Submitted by Unit`
3. `Approved`
4. `Paid` (otomatis saat payment valid)
5. `Needs Correction`
6. `Cancelled`

Aturan:
1. `Rumba Admin Unit` membuat dan submit invoice unit sendiri.
2. Nilai diskon di atas batas kebijakan wajib approval `Rumba Admin Utama`.
3. Pembatalan invoice submit hanya oleh `Rumba Admin Utama`.
4. Revisi pasca-submit lewat `Cancel + Amend` dengan alasan wajib.

SLA:
1. Invoice dibuat maksimal H+1 setelah `Ready to Invoice`.
2. Verifikasi payment entry maksimal H+1 sejak bukti diterima.

## 2.4 SDM (Recruitment sampai Penempatan)

Urutan status kandidat:
1. `Applied`
2. `Screening`
3. `Interview`
4. `Offer`
5. `Hired`
6. `Rejected`

Urutan status onboarding:
1. `Pre-Boarding`
2. `Active`
3. `Probation Review`
4. `Confirmed`

Aturan:
1. `Rumba HRD` memegang proses SDM, unit hanya mengajukan kebutuhan.
2. Penempatan cabang baru sah setelah status `Active`.
3. Mutasi lintas cabang wajib approval `Rumba Admin Utama` + HRD.

SLA:
1. `Applied -> Interview`: maksimal 5 hari kerja.
2. `Offer -> Active`: maksimal 14 hari kalender.

## 3) RACI (Responsible, Accountable, Consulted, Informed) Ringkas

1. `Rumba Admin Unit`
- Responsible: pendaftaran, operasional harian cabang, submit transaksi unit.
- Accountable: kualitas data operasional cabang.

2. `Rumba Admin Utama`
- Accountable: approval transaksi kritikal, exception policy, audit lintas cabang.

3. `Rumba Tutor`
- Responsible: presensi dan catatan akademik kelas yang diajar.

4. `Rumba HRD`
- Responsible: recruitment, onboarding, mutasi, offboarding.

5. `Rumba Founder`
- Informed: KPI lintas cabang (read-only monitoring).

## 4) Definisi Data Wajib (Minimum Fields)

Semua cabang wajib mengisi field minimum berikut sebelum status dapat naik:
1. Pendaftaran: `Unit`, `Program`, `Jadwal`, `Data Ortu`, `Biaya`, `PIC`.
2. Presensi: `Tanggal`, `Kelas`, `Tutor`, `Jumlah Hadir`, `Catatan`.
3. Invoice: `Customer`, `Item/Biaya`, `Unit`, `Due Date`, `Approver` (jika wajib).
4. SDM: `Posisi`, `Unit Penempatan`, `Tanggal Mulai`, `Atasan`, `Status Kontrak`.

## 5) Kontrol Konsistensi Antar Cabang

1. Gunakan template workflow tunggal di ERPNext (jangan duplikasi per cabang).
2. Semua naming status dikunci sesuai daftar di dokumen ini.
3. Audit mingguan: sampling minimal 10 transaksi/cabang.
4. Dashboard KPI wajib menampilkan:
- rata-rata lead time pendaftaran,
- kepatuhan SLA presensi,
- aging invoice,
- status rekrutmen.
5. Cabang dengan kepatuhan <95% masuk daftar pembinaan proses.

## 6) Exception Handling

1. Kondisi exception: gangguan sistem, data legal belum lengkap, force majeure.
2. Exception wajib isi:
- alasan,
- dampak,
- rencana pemulihan,
- target tanggal normalisasi.
3. Exception > 2 hari kerja wajib eskalasi ke `Rumba Admin Utama`.

## 7) Checklist Implementasi

1. Sinkronkan workflow ERPNext dengan status pada dokumen ini.
2. Terapkan validasi mandatory fields per status.
3. Aktifkan approval rule untuk transaksi kritikal.
4. Training `Rumba Admin Unit`, `Tutor`, `HRD` dengan skenario nyata.
5. Jalankan UAT pada 1 cabang pilot selama 1 minggu.
6. Rollout bertahap ke seluruh cabang dan monitor KPI 30 hari pertama.

## 8) Mekanisme Review Berkala

1. Review bulanan lintas cabang oleh `Rumba Admin Utama` + HRD + perwakilan unit.
2. Perubahan workflow hanya lewat revisi dokumen ini (versioned).
3. Setiap perubahan wajib punya tanggal efektif dan PIC implementasi.
