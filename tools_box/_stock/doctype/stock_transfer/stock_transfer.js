// Copyright (c) 2018, Convergenix and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stock Transfer', {
    refresh: function (frm) {
		frm.set_query("item_code", "stock_transfer_item", function() {
			return {
				filters: {
					'is_sales_item':1,
				}
			}
		});

        if (cur_frm.doc.docstatus == 1) {
            frm.add_custom_button(__('General Ledger'), function () {
                frappe.set_route('query-report', 'General Ledger');
            }, __("Accounting Report"));

            frm.add_custom_button(__('Stock Ledger'), function () {
                frappe.set_route('query-report', 'Stock Ledger', {location: cur_frm.doc.location});
            }, __("Stock"));

            frm.add_custom_button(__('Way Bill'), function () {
                 frappe.call({
                        method: "tools_box._stock.doctype.stock_transfer.stock_transfer.make_way_bill",
                        args: {
                            docname: cur_frm.doc.name
                        },
                        callback: function (r) {
                            frappe.model.sync(r.message);
                            frappe.set_route('Form', 'Way Bill', r.message.name);
                        }
                    });
            }, __("Make"));
        }
    }
});
