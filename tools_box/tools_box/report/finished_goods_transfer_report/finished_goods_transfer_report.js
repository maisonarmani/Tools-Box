// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Finished Goods Transfer Report"] = {
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
			"fieldname":"shift",
			"label": __("Shift"),
			"fieldtype": "Select",
			"options": "All\nMorning\nAfternoon\nNight",
			"default":"All",
			"reqd":1
		},
		{
			"fieldname":"item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"reqd":0
		},
		{
			"fieldname":"item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group",
			"reqd":0
		}
	]
}
