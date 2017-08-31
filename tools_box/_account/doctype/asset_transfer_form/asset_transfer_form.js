// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Transfer Form', {
    onload: function (frm) {
        frm.set_query("approved_by", function () {
            return {
                query: "tools_box._hr.doctype.staff_requisition_form.staff_requisition_form.get_approvers"
            };
        });

    },
    refresh: function (frm) {
        var item_grouper = function (p) {
            return {filters: {item_group: p}}
        };
        frm.fields_dict.item.get_query = item_grouper("Fixed Assets");
    }
});
