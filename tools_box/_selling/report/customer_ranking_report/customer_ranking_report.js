// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Ranking Report"] = {
	"filters": [{
            fieldname: "from",
            label: __("Report From"),
            fieldtype: "Date",
			reqd:1
        },
        {
            fieldname: "to",
            label: __("Report To"),
            fieldtype: "Date",
			reqd:1
        }
	]
}
