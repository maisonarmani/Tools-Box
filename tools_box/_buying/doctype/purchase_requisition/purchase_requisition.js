// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

cur_frm.add_fetch("approved_by", "employee_name", "approved_by_name");
cur_frm.add_fetch("authorized_by", "employee_name", "authorized_by_name");

function calcTotal(frm, doctype, docname) {
    var rate = frappe.model.get_value(doctype, docname, "rate");
    var qty = frappe.model.get_value(doctype, docname, "qty");
    if ((rate > 0) && (qty > 0)) {
        frappe.model.set_value(doctype, docname, "amount", isNaN(rate * qty) ? 0 : rate * qty)
    }

    // calc total purchase amount
    var total_amount = 0;
    cur_frm.doc.items.forEach(function (item) {
        total_amount += item.amount;
    });

    frappe.model.set_value(frm.doctype, frm.docname, "total", isNaN(total_amount) ? 0 : total_amount)

}


function get_employees() {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}


function validate(ref_name, parent) {
    var r = frappe.model.get_list("Purchase Requisition Item", {item_code: ref_name});
    if (r.length > 0 && r[0].name != parent) {
        //frappe.model.set_value("Vehicle Schedule Inbound Item",parent,"ref_name", "");
        frappe.throw("Sorry, Duplicate Entry " + ref_name);
    }
}

frappe.ui.form.on('Purchase Requisition', {
    refresh: function (frm) {
        var status = frm.doc.status;
        var can_create_po = frappe.user_roles.includes("Purchase User");
        if ((status == "Authorized" && can_create_po)) {
            cur_frm.add_custom_button(
                __("Make Purchase Order"), function () {
                    // do some kind of mapping and create a new purchase order
                    frappe.call({
                        method: "tools_box._buying.doctype.purchase_requisition.purchase_requisition.make_purchase_order",
                        args: {
                            docname: cur_frm.doc.name
                        },
                        callback: function (r) {
                            frappe.model.sync(r.message);
                            frappe.set_route('Form', 'Purchase Order', r.message.name);
                        }
                    });
                }
            )
        }

        frm.set_query("requested_by", get_employees);

    },
    requested_by: function (frm) {
        if (frm.doc.requested_by && frm.doc.requested_by != "") {
            frappe.call({
                method: "tools_box.controllers.api.get_approver_authorizer",
                args: {
                    emp: frm.doc.requested_by
                },
                callback: function approver(ret) {
                    if (ret.message != undefined) {
                        // Reset value for vehicle and throw exception
                        if (ret.message[0].authorizer && !ret.message[0].approver){
                            frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "approved_by", ret.message[0].authorizer);
                            frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "approved_by_name", ret.message[0].authorizer_name);
                            frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "approver_id", ret.message[0].authorizer_user_id);
                        }else{
                            frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "approved_by", ret.message[0].approver);
                            frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "approved_by_name", ret.message[0].approver_name);
                            frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "approver_id", ret.message[0].approver_id);
                        }
                    }
                }
            })
        }
    }
});

frappe.ui.form.on('Purchase Requisition Item', {
    qty: function (frm, doctype, docname) {
        calcTotal(frm, doctype, docname);
    },
    rate: function (frm, doctype, docname) {
        calcTotal(frm, doctype, docname);
    },
    item_code: function (frm, doctype, docname) {
        validate(frappe.model.get_value(doctype, docname, 'item_code'), docname)
    }
});
