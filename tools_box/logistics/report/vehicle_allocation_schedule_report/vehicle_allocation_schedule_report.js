// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Allocation Schedule Report"] = {
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
                        fieldname: "vehicle",
                        label: __("Vehicle"),
                        fieldtype: "Link",
                        options: "Vehicle",
                },
        {
                        fieldname: "driver",
                        label: __("Driver"),
                        fieldtype: "Link",
                        options: "Driver",
                },
        {
                        fieldname: "delivery_note",
                        label: __("Delivery Note"),
                        fieldtype: "Link",
                        options: "Delivery Note",
                },
	]
}
