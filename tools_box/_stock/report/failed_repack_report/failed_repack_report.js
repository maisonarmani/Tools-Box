// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Failed Repack Report"] = {
	"filters": [{
        "fieldname": "from",
        "label": __("From"),
        "fieldtype": "Date",
        "default": frappe.datetime.year_start(),
        "reqd": 1
    },{
        "fieldname": "to",
        "label": __("To"),
        "fieldtype": "Date",
        "default": frappe.datetime.now_datetime(),
        "reqd": 1
    }]
}
