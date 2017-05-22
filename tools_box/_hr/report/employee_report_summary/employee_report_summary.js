// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Report Summary"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("Leave Start Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.year_start()
		},
		{
			"fieldname":"to_date",
			"label": __("Leave End Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.year_end()
		},
		{
			"fieldname":"gender",
			"label": __("Gender"),
			"fieldtype": "Select",
			"default": "All",
			"options": ["All","Male","Female"],
			"reqd":1
		},
		{
			"fieldname":"leave_type",
			"label": __("Leave Type"),
			"fieldtype": "Link",
			"options": "Leave Type",
			"reqd":1
		},
		{
			"fieldname":"employment_type",
			"label": __("Employment Type"),
			"fieldtype": "Link",
			"options": "Employment Type",
			"reqd":1
		},
		{
			"fieldname":"deparment",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		},
	]
}
