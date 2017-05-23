// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Authority to Load', {
	onload:function(){

	},
	refresh: function(frm) {
		var doc = frm && frm.doc;
		if (doc.__islocal && doc.docstatus == 0) {
			frm.cscript.sales_order_btn();
		}

		$.each(frm.fields_dict,function(i,v){
			frm.set_df_property(i, "read_only", 1);
		});

	}
});


cur_frm.cscript.sales_order_btn = function() {
	cur_frm.add_custom_button(__('Sales Order'),
		function () {
			erpnext.utils.map_current_doc({
				method: "erpnext.selling.doctype.sales_order.sales_order.make_authority_to_load",
				source_doctype: "Sales Order",
				get_query_filters: {
					docstatus: 1,
					status: ["!=", "Closed"],
					per_billed: ["<", 99.99],
					customer: cur_frm.doc.customer || undefined,
					company: cur_frm.doc.company,
					atl: 0
				}
			})
		}, __("Get items from")
	);
};