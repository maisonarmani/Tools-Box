// Copyright (c) 2016, bobzz.zone@gmail.com, masonrmani38@gmail.colm and contributors
// For license information, please see license.txt

frappe.query_reports["Expense Claim Report"] = {
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
            fieldname: "approver",
            label: __("Approver"),
            fieldtype: "Link",
            options: "User"
        },
        {
            fieldname: "expense_type",
            label: __("Expense Claim Type"),
            fieldtype: "Link",
            options: "Expense Claim Type",
        },
        {
            fieldname: "cost_center",
            label: __("Cost Center"),
            fieldtype: "Link",
            options: "Cost Center",
        },
        {
            fieldname: "include_authorized",
            label: __("Include Authorizer"),
            fieldtype: "Check",
        },
    ],
    onload: function(report) {
        //query: "erpnext.hr.doctype.expense_claim.expense_claim.get_expense_approver"
    }
};
