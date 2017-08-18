// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contractor Permit to Work', {
    refresh: function (frm) {
        frm.set_query("approver", function () {
            return {
                query: "tools_box.safety_and_compliance.doctype.contractor_permit_to_work.contractor_permit_to_work.get_approvers",
                filters: {
                    'role': 'Directors'
                }
            };
        });

    }
});
