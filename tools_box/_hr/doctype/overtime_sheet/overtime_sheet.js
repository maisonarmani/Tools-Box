// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt


var DaysBetween = function (date1, date2) {
    //Get 1 day in milliseconds
    var one_day = 1000 * 60 * 60 * 24;
    // try reconverting to real date
    if (!(date1 instanceof Date)) {
        date1 = new Date(date1.replace(" ", "T"));
        date2 = new Date(date2.replace(" ", "T"));
    }
    // Convert both dates to milliseconds
    var date1_ms = date1.getTime();
    var date2_ms = date2.getTime();

    // Calculate the difference in milliseconds
    var difference_ms = date2_ms - date1_ms;
    //take out milliseconds
    difference_ms = difference_ms / 1000;
    //var seconds = Math.floor(difference_ms % 60);
    difference_ms = difference_ms / 60;
    var minutes = Math.floor(difference_ms % 60);
    difference_ms = difference_ms / 60;
    var hours = Math.floor(difference_ms % 24);
    var days = Math.floor(difference_ms / 24);


    return days + ' day(s), ' + hours + ' hour(s) and ' + minutes + ' minute(s)';
};

frappe.ui.form.on('Overtime Sheet', {
    refresh: function (frm, dtype, dname) {
        compute_duration(frm, dtype, dname);
        if (frm.doc.docstatus == 1) {
            frm.add_custom_button(
                __("Expense Claim"), function () {
                    frappe.call({
                        method: "tools_box._hr.doctype.overtime_sheet.overtime_sheet.make_expense_claim_new",
                        args: {
                            docname: frm.doc.name
                        },
                        callback: function (r) {
                            var doc = frappe.model.sync(r.message);
                            frappe.set_route('Form', 'Expense Claim', r.message.name);
                        }
                    });

                }, __("Make"));
            frm.page.set_inner_btn_group_as_primary(__("Make"));
        }
    },
    start_time: function (frm, dtype, dname) {
        compute_duration(frm, dtype, dname)
    },
    end_time: function (frm, dtype, dname) {
        compute_duration(frm, dtype, dname)
    },
});

frappe.ui.form.on('Overtime Sheet Item', {
    amount: calc_total,
    employee: calc_total,
    overtime_information_remove: calc_total,
    overtime_information_add: calc_total,
    start_time: function (frm, dtype, dname) {
        compute_duration(frm, dtype, dname)
    },
    end_time: function (frm, dtype, dname) {
        compute_duration(frm, dtype, dname)
    },
});

function compute_duration(frm, dtype, dname) {
    var st = frappe.model.get_value(dtype, dname, "start_time");
    var et = frappe.model.get_value(dtype, dname, "end_time");
    if (st && et) {
        var dur = DaysBetween(st, et);
        frappe.model.set_value(dtype, dname, "duration", dur);
    }
}

function calc_total(frm) {
    var total_amount = 0;
    var items = cur_frm.doc.overtime_information;
    items.forEach(function (_) {
        total_amount += _.amount || 0;
    });

    frappe.model.set_value(frm.doctype, frm.docname, "total", format_currency(total_amount))
}