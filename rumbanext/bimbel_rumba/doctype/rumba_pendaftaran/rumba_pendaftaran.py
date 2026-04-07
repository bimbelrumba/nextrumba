import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class RumbaPendaftaran(Document):
	def autoname(self):
		branch_code = self._get_branch_code_for_naming()
		date_segment = frappe.utils.now_datetime().strftime("%y%m")
		# Format: REG-[KODE CABANG]-.YYMM.-.####
		prefix = f"REG-{branch_code}-.{date_segment}.-."
		self.name = make_autoname(prefix + "####")

	def validate(self):
		if not self.tanggal_pendaftaran:
			self.tanggal_pendaftaran = frappe.utils.now()

		if self.status_verifikasi in ("Terverifikasi", "Dikonversi") and not self.diverifikasi_oleh:
			self.diverifikasi_oleh = frappe.session.user
			self.tanggal_verifikasi = frappe.utils.now()

		if self.status_verifikasi == "Dikonversi" and not self.murid:
			frappe.throw(_("Status Dikonversi hanya boleh digunakan setelah data Murid terbentuk."))

	@frappe.whitelist()
	def mark_terverifikasi(self, catatan_verifikasi=None):
		self.status_verifikasi = "Terverifikasi"
		self.catatan_verifikasi = catatan_verifikasi or self.catatan_verifikasi
		self.diverifikasi_oleh = frappe.session.user
		self.tanggal_verifikasi = frappe.utils.now()
		self.save()
		return self.name

	@frappe.whitelist()
	def mark_ditolak(self, catatan_verifikasi=None):
		self.status_verifikasi = "Ditolak"
		self.catatan_verifikasi = catatan_verifikasi or self.catatan_verifikasi
		self.diverifikasi_oleh = frappe.session.user
		self.tanggal_verifikasi = frappe.utils.now()
		self.save()
		return self.name

	@frappe.whitelist()
	def convert_to_murid(self):
		if self.status_verifikasi != "Terverifikasi":
			frappe.throw(_("Pendaftaran harus berstatus Terverifikasi sebelum dikonversi."))

		if self.murid:
			return self.murid

		target_doctype = self._resolve_murid_doctype()
		if not target_doctype:
			frappe.throw(
				_("DocType Murid tidak ditemukan. Pastikan DocType target tersedia (contoh: Rumba Murid / Murid).")
			)

		customer = self._ensure_customer_for_invoicing()
		murid_doc = self._create_murid_doc(target_doctype, customer.name if customer else None)

		self.murid = murid_doc.name
		self.status_verifikasi = "Dikonversi"
		self.save()
		return murid_doc.name

	def _resolve_murid_doctype(self):
		candidates = [self.target_murid_doctype, "Rumba Murid", "Murid", "Student"]
		for candidate in candidates:
			if candidate and frappe.db.exists("DocType", candidate):
				self.target_murid_doctype = candidate
				return candidate
		return None

	def _create_murid_doc(self, target_doctype, customer_name):
		murid_doc = frappe.new_doc(target_doctype)
		murid_meta = frappe.get_meta(target_doctype)

		possible_map = {
			"nama_lengkap": self.nama_lengkap_anak,
			"nama_murid": self.nama_lengkap_anak,
			"student_name": self.nama_lengkap_anak,
			"first_name": self.nama_lengkap_anak,
			"nama_panggilan": self.nama_panggilan_anak,
			"birth_place": self.tempat_lahir,
			"date_of_birth": self.tanggal_lahir,
			"gender": self.jenis_kelamin,
			"agama": self.agama_kepercayaan,
			"religion": self.agama_kepercayaan,
			"address": self.alamat_anak,
			"alamat": self.alamat_anak,
			"branch": self.lokasi_rumba,
			"nomor_induk_murid": self.nomor_induk_murid,
			"student_id": self.nomor_induk_murid,
			"school": self.sekolah,
			"kelas": self.kelas_sekolah,
			"grade": self.kelas_sekolah,
			"parent_name": self.nama_ortu_wali,
			"guardian_name": self.nama_ortu_wali,
			"mobile_no": self.nomor_handphone_ortu_wali,
			"student_mobile_number": self.nomor_handphone_ortu_wali,
			"email": self.email_ortu_wali,
			"customer": customer_name,
			"customer_name": customer_name,
		}

		for fieldname, value in possible_map.items():
			if value and murid_meta.has_field(fieldname):
				murid_doc.set(fieldname, value)

		murid_doc.insert(ignore_permissions=True)
		return murid_doc

	def _ensure_customer_for_invoicing(self):
		if self.customer and frappe.db.exists("Customer", self.customer):
			return frappe.get_doc("Customer", self.customer)

		customer_label = f"{self.nama_ortu_wali} (Ortu {self.nama_lengkap_anak})"
		existing_customer = frappe.db.get_value("Customer", {"customer_name": customer_label}, "name")
		if existing_customer:
			self.customer = existing_customer
			self._ensure_customer_address(existing_customer)
			return frappe.get_doc("Customer", existing_customer)

		customer = frappe.new_doc("Customer")
		customer.customer_name = customer_label
		if frappe.get_meta("Customer").has_field("customer_type"):
			customer.customer_type = "Individual"
		customer.insert(ignore_permissions=True)

		self.customer = customer.name
		self._ensure_customer_address(customer.name)
		return customer

	def _ensure_customer_address(self, customer_name):
		if not self.alamat_anak and not self.alamat_tagihan:
			return

		existing_address = frappe.db.exists(
			"Dynamic Link",
			{
				"parenttype": "Address",
				"link_doctype": "Customer",
				"link_name": customer_name,
			},
		)
		if existing_address:
			return

		alamat = self.alamat_tagihan or self.alamat_anak
		address = frappe.new_doc("Address")
		address.address_title = customer_name
		address.address_type = "Billing"
		address.address_line1 = alamat
		if frappe.get_meta("Address").has_field("country"):
			address.country = "Indonesia"
		if frappe.get_meta("Address").has_field("city"):
			address.city = self.tempat_lahir or "-"
		address.append(
			"links",
			{
				"link_doctype": "Customer",
				"link_name": customer_name,
			},
		)
		address.insert(ignore_permissions=True)

	def _get_branch_code_for_naming(self):
		branch_code = self.kode_cabang
		if not branch_code and self.lokasi_rumba:
			branch_code = frappe.db.get_value("Branch", self.lokasi_rumba, "rumba_branch_code")
		if not branch_code and self.lokasi_rumba:
			branch_code = self.lokasi_rumba
		if not branch_code:
			frappe.throw(_("Kode cabang belum tersedia. Isi lokasi cabang terlebih dulu."))

		branch_code = frappe.scrub(str(branch_code)).replace("_", "-").upper()
		return branch_code
