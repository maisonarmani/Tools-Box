// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overtime Sheet', {
    refresh: function (frm) {
        //frm.doc.worflow_state = "Approved";
        if (frm.doc.worflow_state == "Approved") {
            frm.add_custom_button(
                __("Expense Claim"), function () {
                    frappe.call({
                        method: "tools_box._hr.doctype.overtime_sheet.overtime_sheet.make_expense_claim_new",
                        args: {
                            docname: frm.doc.name
                        },
                        callback: function (r) {
                            var doc = frappe.model.sync(r.message);
                            frappe.set_route('Form', 'Expense Claim', r.message.name);
                        }
                    });

            }, __("Make"));
            frm.page.set_inner_btn_group_as_primary(__("Make"));
        }
    }
});

frappe.ui.form.on('Overtime Sheet Item', {
    amount: calc_total,
    employee: calc_total,
    overtime_information_remove: calc_total,
    overtime_information_add: calc_total,
});


function calc_total(frm) {
    var total_amount = 0;
    var items = cur_frm.doc.overtime_information;
    items.forEach(function (_) {
        total_amount += _.amount || 0;
    });

    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "total", format_currency(total_amount))
}