// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

var get_employees = function () {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}
frappe.ui.form.on('Contractor Work Permit Application', {
    onload: function (frm) {
        frm.set_query("supervisor", get_employees);
        if (frm.perm[0].submit == undefined) {
            frm.toggle_display("status", 0)
        }

        if (frm.perm[0].submit && frm.doc.status == 'Approved') {
            frm.add_custom_button('Make Contractor Permit', function () {
                var cwp = frappe.model.make_new_doc_and_get_name('Contractor Work Permit');
                cwp = locals['Contractor Work Permit'][cwp];
                cwp.application_number = cur_frm.doc.name;
                cwp.location = cur_frm.doc.location;
                cwp.supervisor = cur_frm.doc.supervisor;
                cwp.supervisor_name = cur_frm.doc.supervisor_name;
                cwp.company_name = cur_frm.doc.company_name;
                cwp.scope = cur_frm.doc.scope;
                frappe.set_route("Form", "Contractor Work Permit", cwp.name);
            });
        }
    }
});
