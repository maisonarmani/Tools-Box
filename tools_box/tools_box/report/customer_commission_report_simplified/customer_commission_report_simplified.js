// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Customer Commission Report Simplified"] = {
    "filters": [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
			default:frappe.datetime.add_months(frappe.datetime.get_today(),-1),
			reqd:1
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
			default:frappe.datetime.get_today(),
			reqd:1
        },
        {
			fieldname:"item_group",
			label: __("Item Group"),
			default:"Princess",
			options: "Item Group",
			fieldtype: "Link",
            reqd:1 ,
		},
        {
            fieldname: "customer",
            label: __("Customer"),
            fieldtype: "Link",
            options: "Customer",
        },
    ]
};
