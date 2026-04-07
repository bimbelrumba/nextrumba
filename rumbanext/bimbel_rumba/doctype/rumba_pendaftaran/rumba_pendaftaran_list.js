frappe.listview_settings["Rumba Pendaftaran"] = {
	add_fields: ["status_verifikasi", "lokasi_rumba", "nama_lengkap_anak"],
	get_indicator(doc) {
		const colors = {
			"Menunggu Verifikasi": "orange",
			Terverifikasi: "blue",
			Ditolak: "red",
			Dikonversi: "green",
		};
		const status = doc.status_verifikasi || "Menunggu Verifikasi";
		return [__(status), colors[status] || "orange", `status_verifikasi,=,${status}`];
	},
};
