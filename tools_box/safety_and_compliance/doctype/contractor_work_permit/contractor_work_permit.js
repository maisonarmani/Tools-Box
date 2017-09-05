// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contractor Work Permit', {
    refresh: function (frm) {
        frm.set_query("approver", function () {
            return {
                query: "tools_box.safety_and_compliance.doctype.contractor_work_permit.contractor_work_permit.get_approvers",
                filters: {
                    'roles': "('Production Manager', 'Manufacturing Manager','Maintenance Manager','Helpdesk Admin')"
                }
            };
        });
    }
});
