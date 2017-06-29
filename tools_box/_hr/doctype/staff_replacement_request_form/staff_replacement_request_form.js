// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Staff Replacement Request Form', {
	setup:function(frm){
        frm.set_query("approver", function () {
            return {
                query: "tools_box._hr.doctype.staff_replacement_request_form.staff_replacement_request_form.get_approvers"
            };
        });
	},
	refresh: function(frm) {

	}
});
