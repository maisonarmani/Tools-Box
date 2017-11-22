// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item Supplier Report"] = {
	"filters": [
        {
            fieldname: "item",
            label: __("Supplied Item"),
            fieldtype: "Link",
			options:"Item",
            reqd: 0,
			filters:{
            	is_purchase_item:1
			}
        },
        {
            fieldname: "supplier",
            label: __("Supplier"),
            fieldtype: "Link",
			options:"Supplier",
            reqd: 0,
        },
	]
}
