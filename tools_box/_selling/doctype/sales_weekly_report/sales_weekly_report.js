// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Weekly Report', {
    onload: function (frm) {
        cur_frm.fields_dict.sales_person.get_query = function () {
            return {
                filters: {
                    'designation': 'Sales Executive',
                    'status': 'active'
                }
            }
        }
    },
    refresh: function (frm) {
        //.........
    },
    actual_volume_sold: function () {
        var achievement = 0;
        if (cur_frm.doc.target != 0) {
            achievement = (cur_frm.doc.actual_volume_sold / cur_frm.doc.target) * 100
        }
        frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "per_achievement", Math.ceil(achievement))
    },
    sales_person: function (_) {
        if (_.cscript.allow_fetch()) _.cscript.get_target()
    },
    report_from: function (_) {
        if (_.cscript.allow_fetch()) _.cscript.get_target()
    },
    report_to: function (_) {
        if (_.cscript.allow_fetch()) _.cscript.get_target()
    }

});


cur_frm.cscript = {
    allow_fetch: function (frm) {
        var _ = cur_frm.doc;
        return _.report_from && _.report_to && _.sales_person

    }
    , get_target: function (frm) {
        var _ = cur_frm.doc;
        frappe.call({
            method: "tools_box._selling.doctype.sales_weekly_report.sales_weekly_report.get_sales_target",
            args: {
                period_from: _.report_from,
                period_to: _.report_to,
                employee: _.sales_person
            },
            callback: function (r) {
                var weekly_target = r.message[0] ? r.message[0].target / 4 : 0
                frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "target", weekly_target)
            }
        });
    },


    calculate_visted_active: function (frm) {
        var visited = 0;
        var active = 0;
        cur_frm.fields_dict.outlet_type.grid.grid_rows.forEach(function (v, i) {
            if (v.doc.name1 != "") visited++;
            if (v.doc.status == "Active") active++;
        });

        frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "visited", visited)
        frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "active_outlets", active)
    }
};


frappe.ui.form.on('Sales Weekly Report Outlets', {
    name1: function () {
        cur_frm.cscript.calculate_visted_active()
    },
    outlet_type: function () {
        cur_frm.cscript.calculate_visted_active()
    },
    status: function () {
        cur_frm.cscript.calculate_visted_active()
    }
});