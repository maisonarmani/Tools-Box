// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stationaries Issued Report"] = {
    "filters": [{
        "fieldname": "from",
        "label": __("Issued From"),
        "fieldtype": "Datetime",
        "default": frappe.datetime.now_datetime(),
        "reqd": 1
    },{
        "fieldname": "to",
        "label": __("Issued To"),
        "fieldtype": "Datetime",
        "default": frappe.datetime.now_datetime(),
        "reqd": 1
    },{
        "fieldname": "item",
        "label": __("Issued Item"),
        "fieldtype": "Link",
        "options":"Item",
        "reqd": 0,
        "filters":{
            "item_group":"Stationaries"
        }
    },{
        "fieldname": "departmen",
        "label": __("Department"),
        "fieldtype": "Link",
        "options":"Department",
        "reqd": 0
    }
    ]
}
