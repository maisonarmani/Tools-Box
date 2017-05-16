// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Quality Control Material Acceptance Form', {
	refresh: function(frm) {
cur_frm.add_fetch("item_code","stock_uom","pack_size");
cur_frm.add_fetch("item_code","item_name","item_name");
cur_frm.add_fetch("item_code","description","description");
cur_frm.add_fetch("supplier","supplier_name","supplier_name");
cur_frm.fields_dict['address_id'].get_query = function(doc, cdt, cdn) {
	return {
		filters: { 'supplier': doc.supplier}
	}
}

cur_frm.fields_dict['contact_id'].get_query = function(doc, cdt, cdn) {
	return {
		filters: { 'supplier': doc.supplier }
	}
}
frappe.ui.form.on_change("Quality Control Material Acceptance Form", "address_id", function(){
	erpnext.utils.get_address_display(cur_frm, 'address_id', 'address_display');
});
frappe.ui.form.on_change("Quality Control Material Acceptance Form", "contact_id", function(){
  erpnext.utils.get_contact_details(cur_frm);	
});
	}
});
