// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Authority to Load', {
    onload: function () {

    },
    refresh: function (frm) {
        var doc = frm && frm.doc;
        if (doc.__islocal && doc.docstatus == 0) {
            frm.cscript.sales_order_btn();
        }

        $.each(frm.fields_dict, function (i, v) {
            if (i != "delivery_date") {
                frm.set_df_property(i, "read_only", 1);
            }
        })
    }
});


cur_frm.cscript.sales_order_btn = function () {
    this.frm.add_custom_button(__('Sales Order'),
        function () {
            erpnext.utils.map_current_doc({
                method: "erpnext.selling.doctype.sales_order.sales_order.make_delivery_note",
                source_doctype: "Sales Order",
                target: me.frm,
                setters: {
                    customer: me.frm.doc.customer || undefined,
                },
                get_query_filters: {
                    docstatus: 1,
                    status: ["!=", "Closed"],
                    per_delivered: ["<", 99.99],
                    company: me.frm.doc.company,
                    project: me.frm.doc.project || undefined,
                }
            })
        }, __("Get items from"));
};