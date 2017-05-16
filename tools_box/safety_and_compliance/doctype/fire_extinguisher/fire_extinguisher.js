// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fire Extinguisher', {
	refresh: function(frm) {
		console.log(frm);
		// if you are the manager and the fire extinguisher actually needs refill
		if(frappe.user.has_role("Safety And Compliance Manager") && frm.doc.status == 'Empty'){
			var parent = __("");
			cur_frm.add_custom_button("Request for refill", function () {
				//cur_frm.cscript.test_mapping();
				frappe.set_route("Form/Helpdesk Ticket/New Helpdesk Ticket 1", {
				    priority: 'High',
				    request_type: 'Fire Extinguisher Refill',
					description: "Request for refill of Fire Extinguisher" + frm.name
				});
			},parent);
			//cur_frm.page.set_inner_btn_group_as_primary(__("Actions"));

		}
	}
});
