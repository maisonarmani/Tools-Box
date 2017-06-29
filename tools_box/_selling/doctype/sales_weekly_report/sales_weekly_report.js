// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

var take = function (obj, param) {
    var __self__ = this;
    if (typeof param !== 'string') {
        param.forEach(function (val) {
            __self__[val] = obj[val] || "";
        });
    } else {
        __self__[param] = obj[param] || "";
    }
};

frappe.ui.form.on('Sales Weekly Report', {
    onload: function (frm) {
        cur_frm.fields_dict.sales_person.get_query = function () {
            return {
                filters: {
                    enabled: 1
                }
            }
        }
    },
    refresh: function (frm) {
        //.........
    },
    actual_volume_sold: function (_) {
        _.cscript.calculate_achievement()
    },
    sales_person: function (_) {
        if (_.cscript.allow_fetch()) {
            _.cscript.get_target();
            _.cscript.get_visited();
        }
    },
    report_from: function (_) {
        if (_.cscript.allow_fetch()) {
            _.cscript.get_target();
            _.cscript.get_visited();
        }
    },
    report_to: function (_) {
        if (_.cscript.allow_fetch()) {
            _.cscript.get_target();
            _.cscript.get_visited();
        }
    }

});


cur_frm.cscript = {
    allow_fetch: function (frm) {
        var _ = cur_frm.doc;
        if (frappe.datetime.get_day_diff(new Date(_.report_to),new Date(_.report_from)) > 7){
            msgprint("<b>Sorry, this is a weekly report, the difference between start and end date can not " +
                "be greater than 7 days</b>","Invalid Report Date")
            return false;
        }
        return _.report_from && _.report_to && _.sales_person
    },
    get_target: function (frm) {
        var _ = cur_frm.doc;
        frappe.call({
            method: "tools_box._selling.doctype.sales_weekly_report.sales_weekly_report.get_sales_target",
            args: {
                period_from: _.report_from,
                period_to: _.report_to,
                employee: _.sales_person
            },
            callback: function (r) {
                var weekly_target = 0;
                if (r.hasOwnProperty('message')) {
                    var weekly_target = r.message[0].target / 4;
                    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "target", weekly_target)
                } else {
                    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "target", weekly_target)
                }
            }
        });
    },
    calculate_achievement: function () {
        var achievement = 0;
        if (cur_frm.doc.target != 0) {
            achievement = (cur_frm.doc.actual_volume_sold / cur_frm.doc.target) * 100
        }
        frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "per_achievement", Math.ceil(achievement))
    },
    calculate_visted_active: function (frm) {
        var visited = 0;
        var active = 0;
        cur_frm.fields_dict.outlets.grid.grid_rows.forEach(function (v, i) {
            if (v.doc.customer != "") visited++;
            if (v.doc.status == "Active") active++;
        });
        frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "visited", visited)
        frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "active_outlets", active)
    },
    get_visited: function () {
        frappe.call({
            method: 'tools_box._selling.doctype.sales_weekly_report.sales_weekly_report.get_weeks_visits',
            args: {
                "period_from": cur_frm.doc.report_from,
                "period_to": cur_frm.doc.report_to,
                "sales_person": cur_frm.doc.sales_person,
            },
            callback: function (ret) {
                var message = ret.message || undefined;
                cur_frm.doc.outlets = [];
                cur_frm.doc.outlet = [];
                if (message != undefined) {
                    message['existing'].forEach(function (val) {
                        var d = frappe.model.add_child(cur_frm.doc, "Sales Weekly Report Outlets", "outlets");
                        take.apply(d, [val, [
                            "comment", "visited", "customer", "outlet_type"
                        ]]);
                    });
                    message['new'].forEach(function (val) {
                        var d = frappe.model.add_child(cur_frm.doc, "Outlet Details", "outlet");
                        take.apply(d, [val, [
                            "outlet_name", "outlet_type", "address", "contact", "phone", "comments"
                        ]]);
                    });
                    refresh_field('outlets');
                    refresh_field('outlet');
                }

                cur_frm.cscript.calculate_visted_active();
                cur_frm.cscript.calculate_achievement();
            }
        });

    }
};


frappe.ui.form.on('Sales Weekly Report Outlets', {
    customer: function () {
        cur_frm.cscript.calculate_visted_active()
    },
    outlets: function () {
        cur_frm.cscript.calculate_visted_active()
    },
    status: function () {
        cur_frm.cscript.calculate_visted_active()
    }
});