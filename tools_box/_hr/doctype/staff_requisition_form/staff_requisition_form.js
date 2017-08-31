// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
var get_employees = function () {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}
frappe.ui.form.on('Staff Requisition Form', {
    onload: function (frm) {
		frm.set_query("supervisors", get_employees);
        frm.set_query("directors", function () {
            return {
                query: "tools_box._hr.doctype.staff_requisition_form.staff_requisition_form.get_approvers"
            };
        });
    },
	refresh: function(frm) {

	}
});
