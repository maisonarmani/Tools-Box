// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Generator Activity Log Report"] = {
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
			"fieldname":"asset",
			"label": __("Asset"),
			"fieldtype": "Link",
			"options": "Asset",
			"filters": {
					"asset_category":"Plant and Machinery"
				}
		},
	]
}
