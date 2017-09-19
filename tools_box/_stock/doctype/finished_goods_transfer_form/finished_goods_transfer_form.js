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

frappe.ui.form.on('Finished Goods Transfer Form', {
	onload:function(frm){
		frm.set_query('weekly_production_order_form', function(){
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
	weekly_production_order_form: function(frm){
		frappe.call({
			method: "tools_box._stock.doctype.finished_goods_transfer_form.finished_goods_transfer_form.get_producted_items",
			args:{
				production_order:frm.doc.weekly_production_order_form
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
						d.remark = "Excess from manufacturing "+ d.item_name;
						d.description = d.item_name;
					});

					refresh_field('items');
				}
			}
		})
	}



});
