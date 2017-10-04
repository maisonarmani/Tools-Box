// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Daily Cost', {
	refresh: function(frm) {

	}
});

// calculate the total of the items  and
function calc_total(frm){
	var total_cost = 0;
	cur_frm.doc.vehicle_cost_item.forEach(function(_){
		total_cost += _.amount
	});
	frappe.model.set_value(cur_frm.doctype,cur_frm.docname, "total_cost", total_cost)
}

frappe.ui.form.on('Vehicle Daily Cost Item', {
	type:function(frm){
		calc_total(frm)
	},
	amount:function(frm){
		calc_total(frm)
	}
});
