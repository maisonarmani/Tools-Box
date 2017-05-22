// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Raw Materials Return Form', {
	refresh: function(frm) {
		cur_frm.add_fetch("item_code","stock_uom","uom");
		cur_frm.add_fetch("item_code","item_name","item_name");
		cur_frm.add_fetch("item_code","description","description");
    	cur_frm.set_query("materials_request_form", function() {
    	    return {
        	    "filters": {
            	    "purpose": "Material Issue",
                	"docstatus": 1
            	}
        	};
    	});
	}
	
});
