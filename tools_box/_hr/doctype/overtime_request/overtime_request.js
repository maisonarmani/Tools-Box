// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt


function DaysBetween(date1, date2) {
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

function get_employees() {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}

frappe.ui.form.on('Overtime Request', {
    refresh:function(frm){
        frm.set_query("requested_by",get_employees);
        if (frm.doc.workflow_state == "Authorized") {
            frm.trigger("make_overtime_sheet");
        }
    },
    make_overtime_sheet: function (frm) {

        cur_frm.add_custom_button(
            __("Overtime Sheet"), function () {
                // create a time sheet
                frappe.call({
                    method: "tools_box._hr.doctype.overtime_request.overtime_request.make_overtime_sheet",
                    args: {
                        docname: cur_frm.doc.name
                    },
                    callback: function (r) {
                        frappe.model.sync(r.message);
                        frappe.set_route('Form', 'Overtime Sheet', r.message.name);
                    }
                });
            },
        __("Make"))
    },
    start_time: function (frm, dtype, dname) {
        compute_duration(frm, dtype, dname)
    },
    end_time: function (frm, dtype, dname) {
        compute_duration(frm, dtype, dname)
    },
    requested_by: function (frm) {
         frappe.call({
            method: "tools_box.controllers.api.get_approver_authorizer",
            args: {
                emp:frm.doc.requested_by
            },
            callback: function approver_authorizer(ret) {
                if (ret.message != undefined) {
                    // Reset value for vehicle and throw exception
                    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "approved_by", ret.message[0].approver);
                    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "authorized_by",  ret.message[0].authorizer);
                    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "approved_by_name", ret.message[0].approver_name);
                    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "authorized_by_name",  ret.message[0].authorizer_name);
                }
            }
        })
    }
});


function compute_duration(frm, dtype, dname) {
    var st = frappe.model.get_value(dtype, dname, "start_time");
    var et = frappe.model.get_value(dtype, dname, "end_time");
    if (st && et) {
        var dur = DaysBetween(st, et);
        frappe.model.set_value(dtype, dname, "duration", dur);
    }
}
