// Copyright (c) 2016, masonarmani38@gmail.colm and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Advance Report"] = {
    "filters": [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default:frappe.datetime.year_start(),
            reqd:1,

        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default:frappe.datetime.get_today(),
            reqd:1
        },
        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            default:'Paid',
            options:[
                "Paid","Unpaid","Retired"
            ]
        },
    ]
};
