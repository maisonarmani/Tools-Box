frappe.listview_settings['Vehicle Schedule'] = {
	add_fields: ["status", "type", "remark"],
	get_indicator: function(doc) {
		var status = {
            "Declined": "red",
            "Awaiting Approval": "orange",
            "Awaiting Purchase Order": "blue",
            "Completed": "green",
            "Delivered": "green"
        }
		return [__(doc.status), status[doc.status], "status,=," + doc.status];
	}
};
