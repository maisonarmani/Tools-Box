// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt
var get_employees = function () {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}
frappe.ui.form.on('Safety Checklist', {
	onload:function(frm){
		frm.set_query("staff_id", get_employees);
	},
	refresh: function(frm) {

	}
});
