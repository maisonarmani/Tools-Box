// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Log Report"] = {
	"filters": [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
        },
        {
            fieldname: "employee",
            label: __("Employee"),
            fieldtype: "Link",
            options: "Employee",
        },
        {
            fieldname: "vehicle",
            label: __("Vehicle"),
            fieldtype: "Link",
            options: "Vehicle",
        },
	]
}
