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

var get_employees = function () {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}

frappe.ui.form.on('Raw Materials Return Form', {
	onload:function(frm){
		frm.set_query('received_by',get_employees);
		frm.set_query('returned_by',get_employees);
		frm.set_query('production_order', function(){
			return {
				filters:{
					status:"Completed",
				}
			}
		})
	},
	refresh: function(frm) {
		cur_frm.add_fetch("item_code","stock_uom","uom");
		cur_frm.add_fetch("item_code","item_name","item_name");
		cur_frm.add_fetch("item_code","description","description");
		cur_frm.add_fetch("production_order","planned_start_date","date");
	},
	production_order: function(frm){
		frappe.call({
			method: "tools_box._stock.doctype.raw_materials_return_form.raw_materials_return_form.get_production_items",
			args:{
				production_order:frm.doc.production_order
			},
			callback:function(ret){
				if (ret != {}){
					var message = ret.message;
					frm.doc.items = []; // clear older data
					message.forEach(function(val){
						var d = frappe.model.add_child(cur_frm.doc, "Raw Materials Return Item", "items");
						take.apply(d,[val,[
							'item_name','uom','item_code','qty'
						]]);
						d.qty=0
						d.remark = "Returning "+ d.item_name + " after production"
						d.description = "Returning "+ d.item_name + " after production"
					});

					refresh_field('items');
				}
			}
		})
	}


	
});
