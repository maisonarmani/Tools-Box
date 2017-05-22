// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fixed Asset Inspection Checklist', {
    onload: function (frm) {
        console.log("Loading...")
    },
    refresh: function (frm) {
        console.log("Refreshing...")
    },
    fixed_asset_class: function () {
        console.log('failure is a part of success...');
        if (cur_frm.doc.fixed_asset_class) {
            cur_frm.fields_dict.item.grid.get_field('fixed_asset').get_query = function () {
                return {
                    "filters": {
                        "asset_category": cur_frm.doc.fixed_asset_class
                    }
                }
            };
        }

    },
    setup: function (frm) {
        console.log("Setting up...");
    }
});

