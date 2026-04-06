# Checklist Eksekusi Kustomisasi Branch (ERPNext UI)

Gunakan checklist ini saat implementasi real. Tandai setiap item setelah selesai.

## A. Persiapan

- [ ] Login menggunakan role `System Manager`.
- [ ] Pastikan eksekusi dilakukan di site `UAT/Staging` terlebih dahulu.
- [ ] Konfirmasi daftar field final sesuai dokumen baseline.
- [ ] Siapkan 1 data branch untuk pengujian.
- [ ] Catat PIC dan waktu mulai implementasi.

## B. Kustomisasi Form `Branch`

- [ ] Buka `Customize Form`.
- [ ] Pilih `DocType = Branch`.
- [ ] Tambahkan `Section Break`: `Identitas Cabang`.
- [ ] Tambahkan `Section Break`: `Alamat dan Lokasi`.
- [ ] Tambahkan `Section Break`: `Kontak Cabang`.
- [ ] Tambahkan `Section Break`: `Operasional`.
- [ ] Tambahkan `Section Break`: `Relasi Master`.

## C. Tambah Field Identitas Cabang

- [ ] `rumba_branch_code` (`Data`, `Reqd`, `Unique`).
- [ ] `rumba_branch_type` (`Select`: `Owned/Franchise/Partnership`, `Reqd`).
- [ ] `rumba_branch_status` (`Select`: `Active/Inactive/Preparation/Closed`, `Reqd`).
- [ ] `rumba_opening_date` (`Date`).

## D. Tambah Field Alamat dan Lokasi

- [ ] `rumba_address_line_1` (`Data`, `Reqd`).
- [ ] `rumba_address_line_2` (`Data`).
- [ ] `rumba_kelurahan` (`Data`).
- [ ] `rumba_kecamatan` (`Data`).
- [ ] `rumba_city` (`Data`, `Reqd`).
- [ ] `rumba_province` (`Data`, `Reqd`).
- [ ] `rumba_postal_code` (`Data`).
- [ ] `rumba_google_maps_url` (`Data`).

## E. Tambah Field Kontak Cabang

- [ ] `rumba_pic_name` (`Data`, `Reqd`).
- [ ] `rumba_pic_phone` (`Data`, `Reqd`).
- [ ] `rumba_pic_email` (`Data`).
- [ ] `rumba_front_office_phone` (`Data`).
- [ ] `rumba_branch_whatsapp` (`Data`).

## F. Tambah Field Operasional

- [ ] `rumba_operational_start` (`Time`).
- [ ] `rumba_operational_end` (`Time`).
- [ ] `rumba_weekly_off_day` (`Select`: `Monday` s.d. `Sunday`).
- [ ] `rumba_classroom_count` (`Int`).
- [ ] `rumba_max_student_capacity` (`Int`).

## G. Tambah Field Relasi Master

- [ ] `rumba_default_warehouse` (`Link -> Warehouse`).
- [ ] `rumba_default_cost_center` (`Link -> Cost Center`).
- [ ] `rumba_default_receivable_account` (`Link -> Account`).
- [ ] `rumba_default_payable_account` (`Link -> Account`).

## H. Simpan dan Rapikan Form

- [ ] Klik `Save` di `Customize Form`.
- [ ] Pastikan urutan field sesuai section.
- [ ] Pastikan tidak ada duplikasi `fieldname`.

## I. Tambah Validasi via `Client Script`

- [ ] Buka `Client Script`.
- [ ] Buat script baru untuk `DT = Branch`, `Enabled = true`, `View = Form`.
- [ ] Tambahkan validasi `operational_end > operational_start`.
- [ ] Tambahkan validasi `rumba_max_student_capacity >= 0`.
- [ ] Tambahkan validasi field wajib saat `rumba_branch_status = Active`.
- [ ] Simpan `Client Script`.

## J. Uji Fungsional (UAT)

- [ ] Uji simpan saat status `Active` tanpa field wajib (harus gagal).
- [ ] Uji simpan saat semua field wajib terisi (harus berhasil).
- [ ] Uji `rumba_max_student_capacity` bernilai negatif (harus gagal).
- [ ] Uji `operational_end <= operational_start` (harus gagal).
- [ ] Uji field `rumba_branch_code` duplikat (harus gagal).

## K. Permission Review

- [ ] Buka `Role Permission Manager` untuk `Branch`.
- [ ] Verifikasi hak `Rumba Admin Utama`.
- [ ] Verifikasi hak `Rumba Admin Unit`.
- [ ] Simpan perubahan permission jika ada.

## L. Sign-off UAT

- [ ] Semua field tampil dan berfungsi sesuai desain.
- [ ] Semua validasi utama lolos uji.
- [ ] PIC UAT menyetujui hasil implementasi.
- [ ] Catat hasil uji (pass/fail) dan temuan.

## M. Go-Live Production

- [ ] Jadwalkan implementasi pada maintenance window.
- [ ] Ulangi langkah B sampai K di production.
- [ ] Lakukan smoke test cepat pada 1 branch production.
- [ ] Konfirmasi ke tim operasional bahwa perubahan aktif.
- [ ] Catat tanggal go-live dan PIC final.
