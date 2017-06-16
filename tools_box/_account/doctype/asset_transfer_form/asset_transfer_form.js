// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Transfer Form', {
	onload: function (frm) {
        console.log("Loading...")
    },
    refresh: function (frm) {
        var item_grouper =  function(p){ return { filters:{ item_group : p } } };
        frm.fields_dict.item.get_query = item_grouper("Fixed Assets");
    }
});
