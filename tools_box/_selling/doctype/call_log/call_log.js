// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Call Log', {
	setup: function(frm) {
		frm.doc.caller=frappe.user_info().fullname;
	}
});
