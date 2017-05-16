// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt
//Filter: <from date> <to date> <supplier> <mode of payment><bank>
frappe.query_reports["Payment Voucher Report"] = {
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
			"fieldname":"supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier"
		},
		{
			"fieldname":"mop",
			"label": __("Mode Of Payment"),
			"fieldtype": "Link",
			"options": "Mode Of Payment"
		},
		{
			"fieldname":"bank",
			"label": __("Bank"),
			"fieldtype": "Link",
			"options": "Account",
			"get_query": function() {
				return {
					"query": "erpnext.controllers.queries.get_account_list",
					"filters": [
						['Account', 'account_type', 'in', 'Bank, Cash'],
						['Account', 'is_group', '=', 0],
					]
				}
			}
		}
	]
}
