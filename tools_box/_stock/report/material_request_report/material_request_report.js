// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Material Request Report"] = {
    "filters": [{
        "fieldname": "from",
        "label": __("Requested From"),
        "fieldtype": "Datetime",
        "default": frappe.datetime.now_datetime(),
        "reqd": 1
    },{
        "fieldname": "to",
        "label": __("Requested To"),
        "fieldtype": "Datetime",
        "default": frappe.datetime.now_datetime(),
        "reqd": 1
    },{
        "fieldname": "item",
        "label": __("Requested Item"),
        "fieldtype": "Link",
        "options":"Item",
        "reqd": 0
    },{
        "fieldname": "item_group",
        "label": __("Item Group"),
        "fieldtype": "Link",
        "options":"Item Group",
        "reqd": 0
    },{
        "fieldname": "status",
        "label": __("Status"),
        "fieldtype": "Select",
        "options":["Ordered","Pending","Partially Ordered"],
        "reqd": 0
    }
    ]
}
