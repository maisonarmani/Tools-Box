// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

var get_employees = function () {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}
frappe.ui.form.on('Staff Replacement Request Form', {
	setup:function(frm){
		frm.set_query("staff_to_be_replaced", get_employees);
		frm.set_query("supervisor", get_employees);
        frm.set_query("approver", function () {
            return {
                query: "tools_box._hr.doctype.staff_replacement_request_form.staff_replacement_request_form.get_approvers"
            };
        });
	},
	refresh: function(frm) {

	}
});
