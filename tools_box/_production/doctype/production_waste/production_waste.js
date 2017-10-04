// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
var take = function(obj,param){
	var __self__ = this;
	if(typeof param !== 'string'){
		param.forEach(function(val){
			__self__[val] = obj[val];
		});
	}else{
		__self__[param] = obj[param];
	}
};

frappe.ui.form.on('Production Waste', {
	refresh: function(frm) {
		frm.set_query('production_order', function(){
			return {
				filters:{
					status:"Completed"
				}
			}
		})
	},
	production_order:function(frm){
		frappe.call({
			method: "tools_box._production.doctype.production_waste.production_waste.get_production_details",
			args:{
				production_order:frm.doc.production_order
			},
			callback:function(ret){
				console.log(ret.message)
				if (ret != {}){
					var message = ret.message;
					frm.doc.issued = []; // clear older data
					frm.doc.manufactured = []; // clear older data

					message.production_items.forEach(function(val){
						var d = frappe.model.add_child(cur_frm.doc, "Production Waste Issued Items", "issued");
						take.apply(d,[val,[
							'item_name','item_uom','item_code','issued','returned', "used", "waste"
						]]);

						d.issued   = !d.issued ? "0" :d.issued;
						d.returned = !d.returned ? "0" :d.returned;
						d.used  = !d.used ? "0" :d.used;
						d.waste = !d.waste ? "0" :d.waste;
					});

					message.manufactured_items.forEach(function(val){
						var d = frappe.model.add_child(cur_frm.doc, "Production Waste Manufactured Items", "manufactured");
						take.apply(d,[val,[
							'item_name','item_uom','item_code','excess','expected', "actual","waste"
						]]);
						d.excess   = !d.excess ? "0" :d.excess;
						d.expected = !d.expected ? "0" :d.expected;
						d.waste  = !d.waste ? "0" :d.waste;
						d.actual = !d.actual ? "0" :d.actual;
					});
					// refresh the item list
					refresh_field('issued');
					refresh_field('manufactured');
				}
			}
		})
	}
});
