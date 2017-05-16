// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Route Activity Report"] = {
	"filters": [
        {
                        fieldname: "from_date",
                        label: __("From Date"),
                        fieldtype: "Datetime",
                },
        {
                        fieldname: "to_date",
                        label: __("To Date"),
                        fieldtype: "Datetime",
                },
        {
                        fieldname: "sales_rep",
                        label: __("Sales Rep"),
                        fieldtype: "Link",
                        options: "Sales Person",
                },
        {
                        fieldname: "route",
                        label: __("Route"),
                        fieldtype: "Link",
                        options: "Territory",
                },

	]
}
