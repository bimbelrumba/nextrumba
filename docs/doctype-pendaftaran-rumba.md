# DocType Rumba Pendaftaran (Draft Implementasi)

Dokumen ini merangkum mapping form Google Form PMB Rumba (versi PDF) ke DocType `Rumba Pendaftaran` pada app `rumbanext`.

## Alur proses

1. Data pendaftaran masuk ke `Rumba Pendaftaran` (manual/import/API).
2. Admin cabang melakukan verifikasi:
- `Menunggu Verifikasi` -> `Terverifikasi` atau `Ditolak`.
3. Jika `Terverifikasi`, admin klik tombol `Konversi ke Murid`.
4. Sistem:
- Membuat/menautkan `Customer` untuk invoicing atas nama orang tua + nama anak.
- Membuat dokumen pada DocType Murid (target default: `Rumba Murid`, fallback: `Murid` atau `Student`).
- Mengubah status menjadi `Dikonversi`.

## Mapping utama dari form

1. Info program:
- Lokasi RUMBA -> `lokasi_rumba`
- Kelas diminati -> `kelas_yang_diminati`
- Pilihan kelas/hari/jam -> `pilihan_kelas`, `pilihan_hari_belajar`, `pilihan_jam_belajar`

2. Info anak:
- Nama lengkap/panggilan -> `nama_lengkap_anak`, `nama_panggilan_anak`
- Tempat/tanggal lahir -> `tempat_lahir`, `tanggal_lahir`
- Jenis kelamin/agama -> `jenis_kelamin`, `agama_kepercayaan`
- Alamat anak -> `alamat_anak`
- Sekolah/kelas -> `sekolah`, `kelas_sekolah`

3. Info orang tua:
- Hubungan dengan anak -> `hubungan_ortu_wali`
- Nama, no HP, email -> `nama_ortu_wali`, `nomor_handphone_ortu_wali`, `email_ortu_wali`
- Pekerjaan/pendidikan/sosmed -> `pekerjaan_ortu_wali`, `pendidikan_terakhir_ortu_wali`, `akun_sosmed_ortu_wali`

4. Invoicing:
- Customer invoice dibentuk dengan pola `Nama Orang Tua (Ortu Nama Anak)`.
- Alamat invoice dari `alamat_tagihan` (jika ada), fallback ke `alamat_anak`.

## Catatan teknis

1. Child table saudara: `Rumba Pendaftaran Saudara`.
2. Tombol aksi di form:
- `Terverifikasi`, `Tolak`, `Konversi ke Murid`.
3. Mapping field ke DocType Murid bersifat adaptif:
- Sistem hanya mengisi field yang memang ada di meta DocType target.
