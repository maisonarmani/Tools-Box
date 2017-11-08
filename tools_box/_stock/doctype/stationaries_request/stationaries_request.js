// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt


var get_employees = function () {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}

frappe.ui.form.on('Stationaries Request', {
    refresh: function (frm) {
        frm.set_query('requested_by', get_employees);
        frm.set_query('item', "items", function () {
            return {
                filters: {
                    item_group: "Stationaries"
                }
            }
        });
    }
});


frappe.ui.form.on('Stationaries Request Item', {
    items_add: calc_total,
    items_remove: calc_total,
    qty: calc_total,
    ppu: calc_total
})

function calc_total(frm, doctype, docname) {
    var total_amount = 0;
    var items = cur_frm.doc.items;
    var ppu = frappe.model.get_value(doctype,docname, 'ppu');
    var qty = frappe.model.get_value(doctype,docname, 'qty');
    frappe.model.set_value(doctype,docname, "pqty", ppu * qty);

    items.forEach(function (_) {
        total_amount += _.pqty || 0;
    });

    frappe.model.set_value(frm.doctype, frm.docname, "total_qty", total_amount)
}


