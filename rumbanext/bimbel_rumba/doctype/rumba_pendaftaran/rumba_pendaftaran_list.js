frappe.listview_settings["Rumba Pendaftaran"] = {
	add_fields: ["status_verifikasi", "lokasi_rumba", "nama_lengkap_anak"],
	get_indicator(doc) {
		const status_color = {
			"Menunggu Verifikasi": "orange",
			Terverifikasi: "blue",
			Ditolak: "red",
			Dikonversi: "green",
		};

		return [__(doc.status_verifikasi || "Menunggu Verifikasi"), status_color[doc.status_verifikasi] || "orange", "status_verifikasi,=," + (doc.status_verifikasi || "Menunggu Verifikasi")];
	},
};
