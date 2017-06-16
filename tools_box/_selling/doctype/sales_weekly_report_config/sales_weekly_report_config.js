// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Weekly Report Config', {
    onload:function(frm){

    },
	refresh:function(frm){

	},
	setup: function(frm) {
        cur_frm.fields_dict["target"].grid.get_field("employee").get_query = function(doc) {
            return {
                filters:{
                    'designation':['Sales Executive',"Sales Manager"]
                }
            }
        }
	}
});
