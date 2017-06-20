// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Staff Requisition Form', {
    onload: function (frm) {
        frm.set_query("supervisors", function () {
            return {
                filters: {
                    'designation' :["like" ,'%Manager%'],
                    'status': 'active'
                }
            }
        });

        frm.set_query("directors", function () {
            return {
                query: "tools_box._hr.doctype.staff_requisition_form.staff_requisition_form.get_approvers"
            };
        });
    },
	refresh: function(frm) {

	}
});
