// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Goods Tracking Report"] = {
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
            fieldname: "customer",
            label: __("Customer"),
            fieldtype: "Link",
            options: "Customer",
        },
        {
            fieldname: "delivery_status",
            label: __("Delivery Status"),
            fieldtype: "Select",
            options: [
                {"value": "Open", "label": __("Open")},
                {"value": "Shipped", "label": __("Shipped")},
                {"value": "Delivered", "label": __("Delivered")},
            ],
        },
    ]
}
