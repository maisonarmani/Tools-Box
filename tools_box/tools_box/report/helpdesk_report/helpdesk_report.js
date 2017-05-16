// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt
//Filter:<from date><to date><request type><status><raised by>			
frappe.query_reports["HelpDesk Report"] = {
	"filters": [
		{
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
			"default": get_today(),
			"reqd":1
		},
		{
			"fieldname":"request",
			"label": __("Request Type"),
			"fieldtype": "Link",
			"options": "Request Type",
			"reqd":0
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "Draft\nOpen\nIn Progress\nAssigned\nOn-Hold\nClose",
			"reqd":0
		},
		{
			"fieldname":"raised",
			"label": __("Raised By"),
			"fieldtype": "Link",
			"options": "Employee",
			"reqd":0
		},
	]
}
