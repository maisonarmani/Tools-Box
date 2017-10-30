// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle Schedule Report"] = {
	"filters": [{
			"fieldname":"from",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd":1
		},
		{
			"fieldname":"to",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd":1
		},
		{
			"fieldname":"vehicle",
			"label": __("Vehicle"),
			"fieldtype": "Link",
			"options": "Vehicle",
			"reqd":0
		},
		{
			"fieldname":"type",
			"label": __("Type"),
			"fieldtype": "Select",
			"reqd":0,
			"default":"Inbound",
			"options": [
				"Inbound","Outbound"
			],
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"reqd":0,
			"default":"In Transit",
			"options": [
				"In Transit","Delivered","Returned"
			],
		},
	]
}
