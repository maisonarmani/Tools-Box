// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Generator Activity Log', {
	refresh: function(frm) {
		cur_frm.add_fetch("carried_out_by","employee_name","employee_name");
	}
});
cur_frm.cscript.stop= function(doc,dt,dn) {
   var d=locals[dt][dn];
   d.total_time= moment(d.stop).diff(moment(d.start),"seconds") / 3600;
refresh_field("total_time",d.name,d.parentfield);
}
cur_frm.cscript.start= function(doc,dt,dn) {
   var d=locals[dt][dn];
   d.total_time= moment(d.stop).diff(moment(d.start),"seconds") / 3600;
refresh_field("total_time",d.name,d.parentfield);
}