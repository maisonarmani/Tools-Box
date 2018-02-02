// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Pay Summary"] = {
	"filters": [

		{
			"fieldname":"status",
			"label": __("Employee Status"),
			"fieldtype": "Select",
			"default": "All",
			"options": ["All", "Active","Left"]

		},
		{
			"fieldname":"employment_type",
			"label": __("Employment Type"),
			"fieldtype": "Link",
			"options": "Employment Type"
		},
		{
			"fieldname":"department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		}
	]
}
