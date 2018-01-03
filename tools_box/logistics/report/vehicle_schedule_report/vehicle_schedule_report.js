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
			"default":"Outbound",
			"options": [
				"Inbound","Outbound", "Operations"
			],
		},
		{
			"fieldname":"ref_name",
			"label": __("Reference Document"),
			"fieldtype": "Link",
			"options": "Purchase Order",
			"get_query": function() {
				//
				var type = frappe.query_report.filters[3].value;
				return {
					"doctype": (type == "Inbound") ? "Purchase Order" : "Delivery Note",
					"filters": {
						docstatus:1
					}
				}
			}
		}
	]
}
