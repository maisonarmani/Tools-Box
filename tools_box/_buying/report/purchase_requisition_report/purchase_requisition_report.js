// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Purchase Requisition Report"] = {
    "filters": [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            reqd: 1,
            default: frappe.datetime.now_date()
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date", reqd: 1,
            default: frappe.datetime.now_date()
        },
        {
            fieldname: "budgeted",
            label: __("Budgeted Expense"),
            fieldtype: "Check",

        }
    ]
}
