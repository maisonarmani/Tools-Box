// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Sales by Product Report"] = {
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
                        fieldname: "item",
                        label: __("Item"),
                        fieldtype: "Link",
                        options: "Item",
                },
        {
                        fieldname: "customer",
                        label: __("Customer"),
                        fieldtype: "Link",
                        options: "Customer",
                },
        {
                        fieldname: "territory",
                        label: __("Territory"),
                        fieldtype: "Link",
                        options: "Territory",
                },
	]
}
