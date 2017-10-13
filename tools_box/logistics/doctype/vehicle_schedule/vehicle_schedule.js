// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

var allowed = {};
var ready = function (frm) {
    var status = frm.doc.status;
    var can_create_po = frappe.user_roles.includes("Purchase User");
    var can_clear = frappe.user_roles.includes("Financial Controller");
    var deliver = frappe.user_roles.includes("Logistics User");

    console.log(can_clear, status)
    if (status == "Completed" && deliver) {
        frm.add_custom_button(
            __("Delivered"), function () {
                frm.__new_state = "Delivered";
                frm.trigger("deliver")
            }, __("Status"));
    }

    else if (status == "Awaiting Approval" && can_clear) {

        console.log(can_clear, status)
        cur_frm.add_custom_button(
            __("Approve"), function () {
                frm.__new_state = "Awaiting Purchase Order";
                frm.trigger("change_status")
            }, __("Status"));

        cur_frm.add_custom_button(
            __("Decline"), function () {
                frm.__new_state = "Declined";
                frm.trigger("change_status")
            }, __("Status"))
    }
    else if ((status == "Awaiting Purchase Order" && can_create_po)) {
        cur_frm.add_custom_button(
            __("Make Purchase Order"), function () {
                // do some kind of mapping and create a new purchase order
                var po = frappe.model.make_new_doc_and_get_name('Purchase Order');
                po = locals['Purchase Order'][po];
                po.vehicle_schedule = frm.doc.name;
                po.transaction_date = frm.doc.date;
                po.supplier = frm.doc.supplier;
                po.company = "Graceco Limited";

                // setup items
                // var items = [];
                // var poi = frappe.model.make_new_doc_and_get_name('Purchase Order Item');
                // var _ = locals['Purchase Order Item'][poi];
                // _.item_code = "GCL0716";
                // _.item_name = "Van Hire & Delivery Service";
                // _.description = "Van Hire & Delivery Service";
                // _.uom = "Nos";
                // _.unit_cost = frm.doc.daily_cost;
                // _.conversion_factor = 1;
                // _.rate = frm.doc.daily_cost;
                // _.amount = frm.doc.daily_cost;
                // _.qty = 1;
                // items.push(_);
                // po.items = items;
                frappe.set_route("Form", "Purchase Order", po.name);
            }
        )
    }

};

frappe.ui.form.on('Vehicle Schedule', {
    onload: ready,
    refresh: ready,
    change_status: function (frm) {
        frappe.confirm(
            'Are you sure you want to submit this document?',
            function () {
                frappe.call({
                    method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.change_status",
                    args: {
                        dt: frm.doctype,
                        dn: frm.docname,
                        status: frm.__new_state
                    },
                    callback: function (ret) {
                        frm.reload_doc()
                    }
                })
            })
    },
    deliver: function (frm) {
        frappe.confirm(
            'Are you sure you want to mark all deliverables as delivered',
            function () {
                frappe.call({
                    method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.deliver",
                    args: {
                        dt: frm.doctype,
                        dn: frm.docname
                    },
                    callback: function (ret) {
                        frm.reload_doc()
                    }
                })
            })
    },
    refresh: function () {
        frappe.call({
            method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.get_allowed",
            callback: function (ret) {
                if (ret.message != undefined) {
                    allowed = ret.message
                }
            }
        })
    },
    vehicle: function (frm) {
        // get the daily cost information from
        if (frm.doc.vehicle == "" || frm.doc.vehicle == "")
            return

        frappe.call({
            method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.get_daily_cost",
            args: {
                vehicle: frm.doc.vehicle
            },
            callback: function get_daily_cost(ret) {
                if (ret.message == undefined) {
                    // Reset value for vehicle and throw exception
                    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "vehicle", "");
                    frappe.throw("Sorry, Vehicle daily cost is not setup for the vehicle.");
                }
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
    vehicle_schedule_outbound_item_add: calc_total,
    vehicle_schedule_outbound_item_remove: calc_total,
    vehicle_schedule_inbound_item_remove: calc_total,
    vehicle_schedule_inbound_item_add: calc_total,
    ref_name: function (frm, dtype, dname) {
        var dt = frappe.model.get_value(dtype, dname, "ref_type");
        var dn = frappe.model.get_value(dtype, dname, "ref_name");
        validate(dn, dname);
        frappe.call({
            method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.get_party",
            args: {
                doctype: dt,
                docname: dn
            },
            callback: function get_total(ret) {
                frappe.model.set_value(dtype, dname, "party", ret == {} ? 0 : ret.message)
                calc_total(frm);
            }
        })
    },
    amount: calc_total,

}

// calculate the total of the items  and
function calc_total(frm) {
    var total_amount = 0;
    var items = cur_frm.doc.vehicle_schedule_outbound_item
    if (cur_frm.doc.type == "Inbound")
        items = cur_frm.doc.vehicle_schedule_inbound_item;

    items.forEach(function (_) {
        total_amount += _.amount || 0;
    });

    if (total_amount > 0) {
        if (cur_frm.doc.type == "Inbound") {
            t = (allowed.inbound / 100 ) * total_amount;
        }
        else {
            t = (allowed.outbound / 100 ) * total_amount;
        }
        // what percentage of total is total cost
        var ratio = (cur_frm.doc.daily_cost / total_amount) * 100;

        // if daily cost is greater than allowed_outbound percentage of the total amount flag it
        var flag = "";
        var remark = "Vehicle's daily cost is " + roundNumber(ratio, 2) + "% of total amount";
        if (cur_frm.doc.daily_cost > t) {
            cur_frm.doc.ratio_ok = 0;
            flag = "Vehicle's daily cost is more than " + allowed[String(cur_frm.doc.type).toLowerCase] + "% of " + format_currency(total_amount)
        } else {
            cur_frm.doc.ratio_ok = 1;
            flag = "Vehicle's daily cost is " + roundNumber(ratio, 2) + "% of " + format_currency(total_amount)
        }

        frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "total_amount", total_amount)
        frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "remark", remark)
        frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "reason", flag)
    }
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
