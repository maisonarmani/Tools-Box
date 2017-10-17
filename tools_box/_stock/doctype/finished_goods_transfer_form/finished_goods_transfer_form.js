// Copyright (c) 2016, masonarmani38@gmail.com and contributors
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

frappe.ui.form.on('Finished Goods Transfer Form', {
	onload:function(frm){
		frm.set_query('received_by',get_employees);
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
	},
	production_order: function(frm){
		frappe.call({
			method: "tools_box._stock.doctype.finished_goods_transfer_form.finished_goods_transfer_form.get_producted_items",
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
							'item_code','qty','uom','item_name'
						]]);
						d.qty=0;
						d.remark = "Excess from manufacturing "+ d.item_name;
						d.description = d.item_name;
					});
					refresh_field('items');
				}
			}
		})
	}

});
