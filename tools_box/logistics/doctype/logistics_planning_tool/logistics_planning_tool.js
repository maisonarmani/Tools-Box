// Copyright (c) 2018, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
var take = function (obj, param) {
    var __self__ = this;
    if (typeof param !== 'string') {
        param.forEach(function (val) {
            __self__[val] = obj[val] || "";
        });
    } else {
        __self__[param] = obj[param] || "";
    }
}


function get_atls(frm) {
	frm.doc.period_end = frm.doc.period_start = frappe.datetime.get_today()
	var last_date = "";
    if (frm.doc.period_start && frm.doc.period_end) {
        frappe.call({
            method: "tools_box.logistics.doctype.logistics_planning_tool.logistics_planning_tool.get_atls",
            args: {
                ps: frm.doc.period_start,
                pe: frm.doc.period_end,
                territory: frm.doc.territory,
				customer: frm.doc.customer,
				include_pending: frm.doc.include_pending

            },
            callback: function (ret) {
                var message = ret.message;
                cur_frm.doc.deliverables = [];
                if (ret.message){
					message.forEach(function (val) {
						var d = frappe.model.add_child(cur_frm.doc, "Logistics Planning Tool Detail", "deliverables");
						take.apply(d, [val, [
							'authority_to_load', 'delivery_date', 'customer', 'territory'
						]]);
						last_date = val.delivery_date
					});
					frappe.model.set_value(frm.doc.doctype, frm.doc.name,"schedule_delivery_date",frappe.datetime.add_days(frappe.datetime.get_today(),2))
					refresh_field('deliverables');
				}else{
                	refresh_field('deliverables');
				}
            }
        });
    }
}

frappe.ui.form.on('Logistics Planning Tool', {
    territory: get_atls,
    customer: get_atls,
	include_pending:get_atls
});
