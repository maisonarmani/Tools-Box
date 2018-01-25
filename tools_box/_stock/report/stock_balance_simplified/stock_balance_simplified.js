// Copyright (c) 2015, masonarmani38@gmail.com and Contributors and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Balance Simplified"] = {
	"filters": [
		{
			"fieldname":"as_at",
			"label": __("As At"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.sys_defaults.year_start_date,
		},
		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"width": "80",
			"reqd":1,
			"options": "Warehouse"
		},
	]
}
