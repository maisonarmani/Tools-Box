// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
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

frappe.ui.form.on('Production Yield Control Form', {
	onload:function(frm){
		frm.set_query('production_order', function(){
			return {
				filters:{
					docstatus:1
				}
			}
		})
	},
	refresh: function(frm) {
		cur_frm.add_fetch("item_code","stock_uom","uom");
		cur_frm.add_fetch("item_code","item_name","item_name");
		cur_frm.add_fetch("item_code","description","description");

	},
	production_order: function(frm){
		frappe.call({
			method: "tools_box._production.doctype.production_yield_control_form.production_yield_control_form.get_yield",
			args:{
				production_order:frm.doc.production_order
			},
			callback:function(ret){
				if (ret != {}){
					var message = ret.message;
					message.forEach(function(val){
						var d = frappe.model.add_child(cur_frm.doc, "Production Yield Control Item", "items");
						take.apply(d,[val,[
							'item_name','uom','item_code','expected_output','actual_output'
						]]);
						d.description = d.item_name;
						d.comments = "Production Variance "+ d.item_name + " after production";
					});

					refresh_field('items');
				}
			}
		})
	}
});
