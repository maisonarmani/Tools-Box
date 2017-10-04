// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt


var get_employees = function () {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}
frappe.ui.form.on('Machine Downtime Monitoring', {
	refresh: function(frm) {
		frm.set_query('operator',get_employees)
	}
});
