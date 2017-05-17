// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Computing Asset Inspection Checklist', {
	refresh: function(frm) {
		cur_frm.add_fetch("employee","employee_name","employee_name");
	}
});
