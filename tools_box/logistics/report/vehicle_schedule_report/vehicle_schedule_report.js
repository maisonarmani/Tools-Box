// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle Schedule Report"] = {
	"filters": [{
			"fieldname":"from",
			"label": __("From Date"),
			"fieldtype": "Datetime",
			"width": "80",
			"reqd":1
		},
		{
			"fieldname":"to",
			"label": __("To Date"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.get_today(),
			"reqd":1
		},
		{
			"fieldname":"type",
			"label": __("Type"),
			"fieldtype": "Select",
			"reqd":0,
			"options": [
				"Inbound","Outbound"
			],
		},
		{
			"fieldname":"vehicle",
			"label": __("Vehicle"),
			"fieldtype": "Link",
			"options": "Vehicle",
			"reqd":0
		},
	]
}
