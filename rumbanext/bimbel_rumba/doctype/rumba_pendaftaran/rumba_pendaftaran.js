frappe.ui.form.on("Rumba Pendaftaran", {
	refresh(frm) {
		if (frm.is_new()) return;

		if (frm.doc.status_verifikasi === "Menunggu Verifikasi") {
			frm.add_custom_button(__("Terverifikasi"), async () => {
				const note = await askNote(__("Catatan Verifikasi (opsional)"));
				await frm.call("mark_terverifikasi", { catatan_verifikasi: note });
				await frm.reload_doc();
			}, __("Verifikasi"));

			frm.add_custom_button(__("Tolak"), async () => {
				const note = await askNote(__("Alasan Penolakan"));
				await frm.call("mark_ditolak", { catatan_verifikasi: note });
				await frm.reload_doc();
			}, __("Verifikasi"));
		}

		if (frm.doc.status_verifikasi === "Terverifikasi" && !frm.doc.murid) {
			frm.add_custom_button(__("Konversi ke Murid"), async () => {
				await frm.call("convert_to_murid");
				await frm.reload_doc();
			}, __("Aksi"));
		}
	},
});

function askNote(label) {
	return new Promise((resolve) => {
		frappe.prompt(
			[{ fieldname: "note", fieldtype: "Small Text", label }],
			(values) => resolve(values.note),
			__("Verifikasi Pendaftaran"),
			__("Simpan")
		);
	});
}
