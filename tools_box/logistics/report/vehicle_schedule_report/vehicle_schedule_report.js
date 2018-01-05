// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle Schedule Report"] = {
    "filters": [
        {
            "fieldname": "from",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default":"2018-01-01",
            "width": "80",
            "reqd": 1
        },
        {
            "fieldname": "to",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "vehicle",
            "label": __("Vehicle"),
            "fieldtype": "Link",
            "options": "Vehicle",
            "reqd": 0
        },
        {
            "fieldname": "type",
            "label": __("Type"),
            "fieldtype": "Select",
            "reqd": 0,
            "default": "Outbound",
            "options": [
                "Inbound", "Outbound", "Operations"
            ],
        },
        {
            "fieldname": "ref_name",
            "label": __("Reference Document"),
            "fieldtype": "Link",
            "options": "Purchase Order",
            "get_query": function () {
                //
                var type = frappe.query_report.filters[3].value;
                return {
                    "doctype": (type == "Inbound") ? "Purchase Order" : "Delivery Note",
                    "filters": {
                        docstatus: 1
                    }
                }
            }
        }
    ],
    "formatter": function (row, cell, value, columnDef, dataContext, default_formatter) {
        // formatter is called on every cell and the formatted values is then returned
        // value contains the first row value from the server like item[index]
        // cell contains the index the current cell definition
        // columnDef contains information about the current cell
        // default_formatter is the default formatter
        if (true){
            const _context = dataContext;
            if (columnDef.df.fieldname == "name") {
                value = _context[columnDef.df.fieldname];
                //columnDef.df.link_onclick =
                    //"frappe.query_reports['Vehicle Schedule Report'].low(" + JSON.stringify(dataContext) + ")";
                columnDef.df.is_tree = true;
            }

            value = default_formatter(row, cell, value, columnDef, dataContext);

            if (!_context.parent && columnDef.df.fieldname == "name") {
                var $value = $(value).css("font-weight", "bold");
                console.log($(value).html())
                value = $value.html()
                console.log(value)
            }
        }


        return value;
    },
    "tree": true,
    "name_field": "name",
    "parent_field": "parent",
    "initial_depth": 3,
    "onload":function(report){
        //console.log(report)
    }
}
