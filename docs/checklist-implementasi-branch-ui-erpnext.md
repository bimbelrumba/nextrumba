# Checklist Implementasi Step-by-Step di ERPNext UI

Dokumen ini adalah panduan eksekusi kustomisasi DocType `Branch` langsung dari UI ERPNext, berdasarkan baseline di `docs/kustomisasi-doctype-branch-rumba.md`.

## 1) Prasyarat

1. Login sebagai user dengan role `System Manager`.
2. Pastikan perubahan dilakukan di site staging/UAT dulu.
3. Pastikan daftar field sudah disetujui (nama field + tipe field).
4. Siapkan 1 data cabang contoh untuk uji.

## 2) Buka Menu Kustomisasi

1. Masuk ke Awesome Bar (tekan `Ctrl + G` atau klik Search).
2. Ketik `Customize Form` lalu buka.
3. Pada field `DocType`, pilih `Branch`.
4. Centang `Is Customizable` jika diminta.

## 3) Tambahkan Section Break agar Form Rapi

1. Pada tabel field, klik `Add Row`.
2. Tambahkan section dengan urutan berikut:
- `Identitas Cabang`
- `Alamat dan Lokasi`
- `Kontak Cabang`
- `Operasional`
- `Relasi Master`
3. Untuk tiap section, set `Field Type = Section Break`.
4. Simpan sementara (`Save`).

## 4) Input Custom Field MVP

Tambahkan field di bawah ini satu per satu pada section yang sesuai.

1. Identitas Cabang:
- `rumba_branch_code` | `Data` | Label: `Rumba Branch Code` | `Reqd` aktif | `Unique` aktif.
- `rumba_branch_type` | `Select` | Label: `Branch Type` | Opsi: `Owned\nFranchise\nPartnership` | `Reqd` aktif.
- `rumba_branch_status` | `Select` | Label: `Branch Status` | Opsi: `Active\nInactive\nPreparation\nClosed` | `Reqd` aktif.
- `rumba_opening_date` | `Date` | Label: `Opening Date`.

2. Alamat dan Lokasi:
- `rumba_address_line_1` | `Data` | Label: `Address Line 1` | `Reqd` aktif.
- `rumba_address_line_2` | `Data` | Label: `Address Line 2`.
- `rumba_kelurahan` | `Data` | Label: `Kelurahan`.
- `rumba_kecamatan` | `Data` | Label: `Kecamatan`.
- `rumba_city` | `Data` | Label: `City` | `Reqd` aktif.
- `rumba_province` | `Data` | Label: `Province` | `Reqd` aktif.
- `rumba_postal_code` | `Data` | Label: `Postal Code`.
- `rumba_google_maps_url` | `Data` | Label: `Google Maps URL`.

3. Kontak Cabang:
- `rumba_pic_name` | `Data` | Label: `PIC Name` | `Reqd` aktif.
- `rumba_pic_phone` | `Data` | Label: `PIC Phone` | `Reqd` aktif.
- `rumba_pic_email` | `Data` | Label: `PIC Email`.
- `rumba_front_office_phone` | `Data` | Label: `Front Office Phone`.
- `rumba_branch_whatsapp` | `Data` | Label: `Branch WhatsApp`.

4. Operasional:
- `rumba_operational_start` | `Time` | Label: `Operational Start`.
- `rumba_operational_end` | `Time` | Label: `Operational End`.
- `rumba_weekly_off_day` | `Select` | Label: `Weekly Off Day` | Opsi: `Monday\nTuesday\nWednesday\nThursday\nFriday\nSaturday\nSunday`.
- `rumba_classroom_count` | `Int` | Label: `Classroom Count`.
- `rumba_max_student_capacity` | `Int` | Label: `Max Student Capacity`.

5. Relasi Master:
- `rumba_default_warehouse` | `Link` | Options: `Warehouse` | Label: `Default Warehouse`.
- `rumba_default_cost_center` | `Link` | Options: `Cost Center` | Label: `Default Cost Center`.
- `rumba_default_receivable_account` | `Link` | Options: `Account` | Label: `Default Receivable Account`.
- `rumba_default_payable_account` | `Link` | Options: `Account` | Label: `Default Payable Account`.

6. Klik `Save` setelah semua field masuk.

## 5) Atur Urutan Field dan Dependensi Tampilan

1. Pastikan field diurutkan sesuai section (identitas > alamat > kontak > operasional > relasi).
2. Jika perlu, set `Depends On` untuk field relasi agar tampil saat `rumba_branch_status` bukan `Closed`.
3. Simpan perubahan.

## 6) Tambahkan Validasi Ringan via Client Script (UI)

1. Buka Awesome Bar, cari `Client Script`.
2. Klik `New`.
3. Set:
- `DT`: `Branch`
- `Enabled`: aktif
- `View`: `Form`
4. Tempel script validasi berikut:

```javascript
frappe.ui.form.on('Branch', {
  validate(frm) {
    if (frm.doc.rumba_operational_start && frm.doc.rumba_operational_end) {
      if (frm.doc.rumba_operational_end <= frm.doc.rumba_operational_start) {
        frappe.throw(__('Operational End harus lebih besar dari Operational Start'));
      }
    }

    if (frm.doc.rumba_max_student_capacity != null && frm.doc.rumba_max_student_capacity < 0) {
      frappe.throw(__('Max Student Capacity tidak boleh negatif'));
    }

    if (frm.doc.rumba_branch_status === 'Active') {
      const required_when_active = [
        'rumba_branch_code',
        'rumba_branch_type',
        'rumba_address_line_1',
        'rumba_city',
        'rumba_province',
        'rumba_pic_name',
        'rumba_pic_phone'
      ];

      required_when_active.forEach(fieldname => {
        if (!frm.doc[fieldname]) {
          frappe.throw(__(`Field ${fieldname} wajib diisi saat status Active`));
        }
      });
    }
  }
});
```

5. Simpan `Client Script`.

## 7) Uji Fungsional dari UI

1. Buka `Branch List` dan pilih satu branch uji.
2. Coba simpan branch dengan `rumba_branch_status = Active` tapi tanpa field wajib.
3. Pastikan sistem menolak simpan dan menampilkan error validasi.
4. Isi seluruh field wajib, lalu simpan ulang.
5. Uji nilai negatif di `rumba_max_student_capacity`.
6. Uji nilai jam `operational_end <= operational_start`.

## 8) Atur Hak Akses Dasar (UI)

1. Buka `Role Permission Manager`.
2. Pilih `DocType: Branch`.
3. Review role berikut:
- `Rumba Admin Utama`: create/read/write.
- `Rumba Admin Unit`: read, write terbatas (jika perlu via permission level).
4. Simpan permission.

## 9) Finalisasi dan Dokumentasi

1. Catat tanggal implementasi, site, dan PIC implementasi.
2. Catat hasil uji (pass/fail) untuk 3 skenario validasi utama.
3. Jika UAT lolos, ulangi langkah yang sama di production pada jadwal maintenance.

## 10) Checklist Sign-off

1. Semua custom field `Branch` berhasil dibuat.
2. Validasi status `Active` berjalan.
3. Validasi jam operasional berjalan.
4. Validasi kapasitas berjalan.
5. Permission dasar role telah direview.
6. UAT branch pilot dinyatakan lulus.
