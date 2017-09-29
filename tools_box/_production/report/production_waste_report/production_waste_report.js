// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Production Waste Report"] = {
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
			"fieldname":"production_order",
			"label": __("Production Order"),
			"fieldtype": "Link",
			"options": "Production Order",
			"reqd":0,
			"filters":{
				status:"Completed"
			}
		},
	]
}
