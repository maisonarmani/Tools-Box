// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Staff Requisition Form', {
    onload: function (frm) {
        frm.fields_dict.supervisor.get_query = function () {
            return {
                filters: {
                    'designation' :["like" ,'%Manager%'],
                    'status': 'active'
                }
            }
        }
    },
	refresh: function(frm) {

	}
});
