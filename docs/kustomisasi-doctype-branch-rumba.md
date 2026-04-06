# Kustomisasi DocType Branch untuk Rumba

Dokumen ini menjadi baseline kustomisasi DocType bawaan ERPNext: `Branch`, agar setiap cabang Rumba punya data profil yang lebih lengkap dan seragam.

## 1) Tujuan

1. Menyimpan profil cabang secara standar lintas unit.
2. Menjadi sumber referensi untuk operasional, keuangan, dan audit.
3. Menjadi pondasi untuk reporting per cabang (status aktif, kapasitas, lokasi, PIC).

## 2) Prinsip Desain

1. Tetap pakai DocType standar `Branch` (tidak membuat DocType baru).
2. Field tambahan memakai prefix `rumba_` untuk menghindari bentrok.
3. Data kritikal dijadikan mandatory saat submit/aktif.
4. Semua cabang menggunakan struktur field yang sama.

## 3) Usulan Struktur Field Tambahan (MVP)

## 3.1 Identitas Cabang

1. `rumba_branch_code` (`Data`, unique, required)
- Kode cabang internal (contoh: `RMB-JKT-SBY01`).

2. `rumba_branch_name` (`Data`, required)
- Nama cabang (contoh: Taman Sari, Selindung)

3. `rumba_branch_type` (`Select`, required)
- Opsi: `Owned`, `Franchise`, `Partnership`.

4. `rumba_branch_status` (`Select`, required)
- Opsi: `Active`, `Inactive`, `Preparation`, `Closed`.

5. `rumba_opening_date` (`Date`)
- Tanggal operasional pertama cabang.

## 3.2 Lokasi

1. `rumba_province` (`Select`)
2. `rumba_city_region` (`Data`)
3. `rumba_address_line_1` (`Small Text`)
4. `rumba_google_maps_url` (`Data`)
5. `rumba_pic_name` (`Data`)
6. `rumba_phone` (`Data`)
7. `rumba_email` (`Data`)
8. `rumba_classroom_count` (`Int`)
9. `rumba_max_student_capacity` (`Int`)

## 3.3 Relasi Master ERPNext

1. `rumba_default_warehouse` (`Link` -> `Warehouse`)
2. `rumba_default_cost_center` (`Link` -> `Cost Center`)
3. `rumba_default_receivable_account` (`Link` -> `Account`)
4. `rumba_default_payable_account` (`Link` -> `Account`)

## 4) Validasi Minimal yang Direkomendasikan

1. `rumba_branch_code` wajib unik.
2. Jika `rumba_branch_status = Active`, maka field berikut wajib terisi:
- `rumba_branch_code`
- `rumba_branch_type`
- `rumba_address_line_1`
- `rumba_city`
- `rumba_province`
- `rumba_pic_name`
- `rumba_pic_phone`

3. `rumba_operational_end` harus lebih besar dari `rumba_operational_start`.
4. `rumba_max_student_capacity` tidak boleh lebih kecil dari 0.

## 5) Implementasi Teknis yang Disarankan

1. Tambahkan field via `Customize Form` pada DocType `Branch`.
2. Export customizations ke app Rumba (fixture) agar versioned di Git.
3. Buat validasi server-side ringan (script/patch) untuk aturan status `Active`.
4. Buat role permission:
- `Rumba Admin Utama`: create/read/write/submit/cancel.
- `Rumba Admin Unit`: read + write terbatas field operasional.

## 6) Urutan Eksekusi (Sprint Awal)

1. Finalisasi nama field + label.
2. Implementasi field MVP (bagian 3.1, 3.2, 3.3).
3. UAT pada 1 cabang pilot.
4. Tambahkan field relasi keuangan (bagian 3.5) setelah chart of accounts final.
5. Rollout semua cabang.

## 7) Catatan Penting

1. Dokumen ini fokus pada `Branch` sebagai master data cabang.
2. Jika nanti butuh data yang sifatnya historis (contoh: perubahan PIC, perubahan kapasitas), sebaiknya dibuat DocType turunan/transaksi agar audit trail lebih rapi.
