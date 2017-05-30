// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Equipment Maintenance Log', {
    onload: function (frm) {
        console.log("Loading...")
    },
    refresh: function (frm) {
        frm.fields_dict.items.grid.get_field('spare_parts_used').get_query = function (doc, cdt, cdn) {
            return {
                filters: {
                    item_group: "Spares Parts",
                }
            };
        };
    }
});
