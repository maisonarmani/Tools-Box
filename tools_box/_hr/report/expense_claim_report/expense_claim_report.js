// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Expense Claim Report"] = {
	"filters": [
		{
			"fieldname":"posting_from",
			"label": __("Posting From"),
			"fieldtype": "Date",
			"width": "80",
			"reqd":1,
			"default":dateutil.year_start()
		},
		{
			"fieldname":"posting_to",
			"label": __("Posting To"),
			"fieldtype": "Date",
			"width": "80",
			"reqd":1,
			"default":moment.tz()._d
		},
		{
			"fieldname":"approval_status",
			"label": __("Approval Status"),
			"fieldtype": "Select",
			"width": "80",
			"reqd":0,
			"options":["All","Draft","Approved","Authorized","IAD Cleared","Rejected"],
		},
		{
			"fieldname":"doc_status",
			"label": __("Document Status"),
			"fieldtype": "Select",
			"width": "80",
			"reqd":0,
			"options":[{label:"Draft", value:0},{label:"Submitted", value:1},{label:"Cancelled", value:2}],
		},
	]
}
