// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stationaries Issued', {
    refresh: function (frm) {
        frm.set_query("item_issued", "items_issued", function () {
            return {
                filters: {
                    item_group: "Stationaries"
                }
            }
        })
    }
});

frappe.ui.form.on('Stationaries Issued Items', {
    received_by: calc_total,
    item_issued: calc_total,
    issued_date: calc_total,
    items_issued_remove: calc_total,
    items_issued_add: calc_total,
    pieces: calc_total,
});


function calc_total(frm) {
    var total_amount = 0;
    var items = cur_frm.doc.items_issued;
    items.forEach(function (_) {
        total_amount += _.pieces || 0;
    });

    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "total_items_issued", format_currency(total_amount))
}