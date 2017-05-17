// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Generator Fuel Consumption Log', {
	refresh: function(frm) {
		cur_frm.add_fetch("generator","asset_name","generator_name");
	},
	setup: function(frm) {
		cur_frm.set_query("generator", function() {
			return {
				"filters": {
					"asset_category":"Plant and Machinery",
					"docstatus":1
				}
			};
		});
		
	},
	
});

cur_frm.cscript.fuel_qty = function(doc,dt,dn) {
   var d=locals[dt][dn];
d.total = d.fuel_qty * d.unit_price;
refresh_field("total",d.name,d.parentfield);
}
cur_frm.cscript.unit_price = function(doc,dt,dn) {
   var d=locals[dt][dn];
d.total = d.fuel_qty * d.unit_price;
refresh_field("total",d.name,d.parentfield);
}