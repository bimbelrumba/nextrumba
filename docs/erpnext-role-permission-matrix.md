# ERPNext Role & Permission Matrix (Rumba)

Dokumen ini menjadi baseline pengaturan Role, User Permission, dan Approval Rule di ERPNext untuk operasional multi-unit/cabang Rumba.

Dokumen terkait:
1. `docs/workflow-standar-semua-cabang.md` untuk standar alur proses lintas cabang.

## 1) Daftar Role

1. `Rumba Admin Unit` (Admin Cabang/Unit)
2. `Rumba Admin Utama` (Admin Utama)
3. `Rumba Founder`
4. `Rumba Tutor`
5. `Rumba HRD`
6. `Rumba Ortu` (Orang Tua)

## 2) Prinsip Akses Utama

1. **Data isolation per unit**: user unit hanya melihat data unit sendiri dengan `User Permission` berbasis field `Company`/`Branch`/`Unit`.
2. **Least privilege**: tiap role hanya dapat akses data/modul sesuai kebutuhan kerja.
3. **Transaksi terkunci setelah submit**: edit/hapus transaksi submit dibatasi ketat.
4. **Auditability**: perubahan transaksi kritikal dilakukan lewat alur `Amend`/`Cancel` + alasan.

## 3) Matrix Akses per Role

Keterangan:
- `R`: Read
- `C`: Create
- `U`: Update
- `D`: Delete
- `S`: Submit/Cancel/Amend (transaksi)
- `-`: tidak ada akses

| Modul / Area | Unit Admin | Super Admin | Founder | Tutor | HRD | Parent |
|---|---|---|---|---|---|---|
| Master Data Unit (Program, Kelas, Jadwal) | R/C/U | R/C/U/D | R | R | R | - |
| Data Murid | R/C/U | R/C/U/D | R (ringkasan) | R (kelas sendiri) | R (terbatas) | R (anak sendiri) |
| Keuangan (Invoice, Payment Entry) | R/C/U/S* | R/C/U/D/S | R (dashboard/laporan) | - | - | R (tagihan anak sendiri) |
| Operasional Kelas & Kehadiran | R/C/U | R/C/U/D | R (ringkasan) | R/C/U (kelas sendiri) | - | R (anak sendiri) |
| SDM (Recruitment, Employee, Onboarding/Exit) | R (unit sendiri) | R/C/U/D | R (ringkasan) | - | R/C/U/D | - |
| Laporan & Dashboard | R (unit sendiri) | R (semua unit) | R (semua unit) | R (kelas sendiri) | R (SDM) | R (anak sendiri) |
| User & Role Management | - | R/C/U/D | - | - | - | - |

Catatan `S*` untuk Unit Admin:
- Boleh submit transaksi **unit sendiri**.
- Tidak boleh cancel/delete transaksi submit tanpa approval Admin Utama.

## 4) Aturan Detail per Role

## 4.1 Rumba Admin Unit

Hak:
1. Membuat transaksi operasional unit (penjualan/biaya/pembayaran) untuk unit sendiri.
2. Mengelola data kelas, jadwal, dan murid unit sendiri.

Batasan:
1. Tidak dapat melihat data unit lain (wajib filter `Unit/Branch/Company`).
2. Tidak bisa `Delete` transaksi yang sudah submit.
3. Edit transaksi submit hanya lewat mekanisme `Amend` dan butuh approval bila nominal/akun berubah.
4. Delete untuk draft transaksi dibatasi (opsional: hanya jika pembuat sendiri).

## 4.2 Rumba Admin Utama

Hak penuh seluruh unit:
1. Akses lintas unit.
2. Dapat edit/cancel/delete transaksi sesuai kebijakan audit.
3. Kelola role, user, dan approval policy.

## 4.3 Rumba Founder

Fokus monitoring:
1. Read-only seluruh unit.
2. Dashboard KPI: jumlah murid aktif, revenue, arus kas, tingkat kehadiran, churn.
3. Tidak dapat membuat/mengubah/menghapus transaksi.

## 4.4 Rumba Tutor

Fokus akademik:
1. Melihat kelas yang dia ajar.
2. Input/edit daftar hadir untuk kelas yang diajar.
3. Melihat profil murid pada kelas yang diajar (tanpa akses keuangan penuh).

## 4.5 Rumba HRD

Fokus SDM end-to-end:
1. Recruitment, employee records, assignment/penempatan, mutasi, offboarding/resign.
2. Akses ke data SDM seluruh unit (atau scoped sesuai kebijakan).
3. Tidak memiliki hak transaksi keuangan operasional kecuali reimburse/payroll area HR yang ditetapkan.

## 4.6 Rumba Ortu (Orang Tua)

Akses portal terbatas:
1. Melihat progress report anak sendiri.
2. Melihat attendance anak sendiri.
3. Melihat tagihan/pembayaran anak sendiri (jika portal billing diaktifkan).
4. Tidak memiliki akses data murid lain.

## 5) Mapping Implementasi ERPNext

## 5.1 User Permission (wajib untuk multi-unit)

Setiap user `Unit Admin`, `Tutor`, dan (opsional) `HRD` diberi `User Permission`:
1. `Company` = unit user
2. `Branch`/`Cost Center` = unit user
3. `Academic Term`/`Program` (opsional sesuai struktur data)

Aktifkan `Apply Strict User Permissions` untuk mencegah bocor lintas unit.

## 5.2 DocType Permission Level

Contoh aturan transaksi keuangan:
1. Draft: Unit Admin `C/U`, `D` (opsional pembuat sendiri).
2. Submitted: Unit Admin `R` saja, perubahan lewat `Amend` + approval.
3. Cancel/Delete Submitted: hanya Super Admin.

## 5.3 Workflow & Approval

Disarankan workflow untuk dokumen kritikal (Sales Invoice, Payment Entry, Expense Claim):
1. `Draft` -> `Submitted by Unit Admin`
2. `Needs Correction` (jika ditolak)
3. `Approved/Cancelled by Super Admin`

Wajib field:
1. `Reason for Amendment/Cancellation`
2. `Approved By`
3. `Approval Timestamp`

## 5.4 Parent Access

Gunakan web portal dengan relasi:
1. Parent -> Student (anak sendiri)
2. Filter report/attendance/invoice berdasarkan relasi ini

## 6) Rekomendasi Kebijakan Edit/Hapus Transaksi

1. **No hard delete** untuk transaksi submit (gunakan cancel + amend).
2. Delete hanya di draft dan maksimal H+1 dari pembuatan (opsional).
3. Semua cancel/amend wajib alasan.
4. Log audit ditinjau periodik oleh Super Admin/Founder.

## 7) Checklist Setup

1. Buat 6 role custom di atas.
2. Set Role Permission Manager per DocType utama.
3. Aktifkan User Permission strict mode.
4. Buat workflow dokumen transaksi.
5. Uji skenario lintas role (UAT) sebelum go-live.
6. Buat dashboard founder dan parent portal view.
