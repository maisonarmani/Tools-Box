// Copyright (c) 2018, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

function add_fetch_child(sdoctype, sdocname,sfield, cdt,cdn, dfield){
    frappe.call({
        method: "frappe.client.get_value",
        args: {
            doctype: sdoctype,
            fieldname: sfield,
            filters: {name: sdocname},
        },
        callback: function (r) {
            if (r.message) {
                frappe.model.set_value(cdt, cdn, dfield, r.message[sfield]);
            }
        }
    });
}

frappe.ui.form.on('Employee Role', {
	refresh: function(frm) {

	}
});



frappe.ui.form.on('Employee Role Item', {
	refresh: function(frm) {

	},

	assessment_area:function(frm,cdt,cdn){
		var assessment_area = frappe.model.get_value(cdt,cdn,"assessment_area")
		add_fetch_child("Assessment Area", assessment_area, "has_numerical_target",cdt,cdn, "has_target");
		add_fetch_child("Assessment Area", assessment_area, "numerical_target", cdt,cdn, "target");
		add_fetch_child("Assessment Area", assessment_area, "target_frequency",cdt,cdn, "target_frequency");
		add_fetch_child("Assessment Area", assessment_area, "allow_in_timesheet", cdt,cdn, "allow_timesheet");
		add_fetch_child("Assessment Area", assessment_area, "activity_type",cdt,cdn, "activity_type");
	}
});
