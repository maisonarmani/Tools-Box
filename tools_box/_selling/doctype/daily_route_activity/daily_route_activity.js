// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

var take = function(obj,param){
	var __self__ = this;
	if(typeof param !== 'string'){
		param.forEach(function(val){
			__self__[val] = obj[val] || "";
		});
	}else{
		__self__[param] = obj[param] || "";
	}
};

frappe.ui.form.on('Daily Route Activity', {
    refresh: function (frm) {

    },
    dra_sales_rep: function (frm) {
        frm.trigger('get_route')
    },
    dra_date: function (frm) {
        frm.trigger('get_route')
    },
    get_route: function (frm) {
        if (frm.doc.dra_date != undefined && frm.doc.dra_sales_rep != undefined) {
            frappe.call({
                method: "tools_box._selling.doctype.sales_journey_plan.sales_journey_plan.get_current_route",
                args: {
                    sales_rep: frm.doc.dra_sales_rep,
                    date: frm.doc.dra_date
                },
                callback: function (r) {
					frm.doc.dra_visits = []
                    if (r.message != undefined) {
                        r.message.forEach(function (val) {
                            var d = frappe.model.add_child(frm.doc, "Daily Route Activity Visit","dra_visits");
                            take.apply(d, [val, ['drav_customer']]);
                        });
				        refresh_field('dra_visits');
                    }
                }
            })
        }
    }
});
