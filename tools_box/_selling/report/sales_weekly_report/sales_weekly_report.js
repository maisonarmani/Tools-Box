// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Weekly Report"] = {
	"filters": [
        {
            fieldname: "report_from",
            label: __("Report From"),
            fieldtype: "Date",
        },
        {
            fieldname: "report_to",
            label: __("Report To"),
            fieldtype: "Date",
        },
        {
            fieldname: "sales_person",
            label: __("Sales Person"),
            fieldtype: "Link",
            options: "Sales Person",
        },
	]
}
