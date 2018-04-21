// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Valuation Report"] = {
	"filters": [
{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.year_start()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.year_end()
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse"
		}
	]
}
