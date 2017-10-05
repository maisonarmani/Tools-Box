// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

var allowed = {};
frappe.ui.form.on('Vehicle Schedule', {
    refresh: function () {
        frappe.call({
            method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.get_allowed",
            callback: function (ret) {
                console.log(ret)
                if (ret.message != undefined) {
                    allowed = ret.message
                }
            }
        })
    },
    vehicle:function (frm) {
        // get the daily cost information from
        frappe.call({
            method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.get_daily_cost",
            args: {
                vehicle: frm.doc.vehicle
            },
            callback: function get_daily_cost(ret) {
                frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "daily_cost", ret == {} ? 0 : ret.message)
            }
        })
    }
});


var item_opts = {
    onload: function (frm) {
        frm.set_query("ref_name", function () {
            return {
                filters: {
                    docstatus: 1
                }
            }
        })
    },
    ref_name: function (frm, dtype, dname) {
        var dt = frappe.model.get_value(dtype, dname, "ref_type");
        var dn = frappe.model.get_value(dtype, dname, "ref_name");
        validate(dn, dname);
        frappe.call({
            method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.get_total",
            args: {
                doctype: dt,
                docname: dn
            },
            callback: function get_total(ret) {
                frappe.model.set_value(dtype, dname, "amount", ret == {} ? 0 : ret.message)
                calc_total(frm);
            }
        })
    },

}

// calculate the total of the items  and
function calc_total(frm) {
    var total_amount = 0;
    var items = cur_frm.doc.vehicle_schedule_outbound_item
    if (cur_frm.doc.type == "Inbound")
        items = cur_frm.doc.vehicle_schedule_inbound_item;

    items.forEach(function (_) {
        total_amount += _.amount
    });


    if (cur_frm.doc.type == "Inbound") {
        t = (allowed.inbound / 100 ) * total_amount;
    }
    else {
        t = (allowed.outbound / 100 ) * total_amount;
    }

    // if daily cost is greater than allowed_outbound percentage of the total amount flag it
    var flag = "";
    if (cur_frm.doc.daily_cost > t) {
        flag = "Vehicle daily cost more than "+allowed[string.toLowerCase(cur_frm.doc.type)]+"% of total amount"
    } else {
        flag = "Ok"
    }

    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "total_amount", total_amount)
    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "remark", flag)
}

function validate(ref_name, parent) {
    // Inbound
    var r = frappe.model.get_list("Vehicle Schedule Inbound Item", {ref_name: ref_name});
    if (r.length > 0 && r[0].name != parent) {
        //frappe.model.set_value("Vehicle Schedule Inbound Item",parent,"ref_name", "");
        frappe.throw("Sorry, Reference name " + ref_name + " already in use");
    }

    // Outbound
    r = frappe.model.get_list("Vehicle Schedule Outbound Item", {ref_name: ref_name});
    if (r.length > 0 && r[0].name != parent) {
        //frappe.model.set_value("Vehicle Schedule Outbound Item",parent,"ref_name", "");
        frappe.throw("Sorry, Reference name " + ref_name + " already in use");
    }
}

frappe.ui.form.on('Vehicle Schedule Outbound Item', item_opts);
frappe.ui.form.on('Vehicle Schedule Inbound Item', item_opts);
