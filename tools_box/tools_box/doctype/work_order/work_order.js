// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
function get_employees() {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}
cur_frm.add_fetch('item_code', 'stock_uom', 'uom');
cur_frm.add_fetch('item_code', 'item_name', 'item_name');
cur_frm.add_fetch('item_code', 'description', 'item_description');
cur_frm.set_query("approver", function () {
    return {
        query: "tools_box.tools_box.doctype.job_card.job_card.get_job_card_approver"
    };
});
cur_frm.set_query("work_order_material_detail", "item_code", function () {
    return {
        filters:{
            is_purchase_item:true
        }
    }
});
frappe.ui.form.on('Work Order', {
    refresh: function (frm) {
        frm.set_query("work_order_completion_verified_by", get_employees);
        frm.set_query("requested_by", get_employees);

        if (cur_frm.doc.status == 'Approved' || true) {
            cur_frm.add_custom_button('Make Purchase Order', function () {
                frappe.model.open_mapped_doc({
                    method: "tools_box.tools_box.doctype.work_oder.work_order.make_purchase_order",
                    frm: cur_frm
                });
            });
        }

        if (!frappe.user.has_role(['Maintenance Admin'])) {
            cur_frm.fields.forEach(function (l) {
                cur_frm.set_df_property(l.df.fieldname, "read_only", (cur_frm.doc.status == 'Approved' || cur_frm.doc.status == 'Completed'));
            })
        }
        else {
            cur_frm.fields.forEach(function (l) {
                cur_frm.set_df_property(l.df.fieldname, "read_only",
                    (cur_frm.doc.status == 'Approved' || cur_frm.doc.status == 'Completed'));
            })
            cur_frm.set_df_property('work_order_completion_date', 'read_only', 0);
            cur_frm.set_df_property('work_order_completion_verified_by', 'read_only', 0);
            cur_frm.set_df_property('approval', 'read_only', 0);
        }

        cur_frm.set_df_property('status', 'read_only', 1);

    },
    ticket_number: function (frm, cdt, cdn) {
        var work_order = frappe.model.get_doc(cdt, cdn);
        if (work_order.ticket_number) {
            frappe.call({
                method: "tools_box.tools_box.doctype.work_order.work_order.get_requested_by",
                args: {
                    ticket_number: work_order.ticket_number
                },
                callback: function (r) {
                    frappe.model.set_value(cdt, cdn, "requested_by", r.message);
                }
            });

            frappe.call({
                method: "tools_box.tools_box.doctype.work_order.work_order.get_employee_name",
                args: {
                    ticket_number: work_order.ticket_number
                },
                callback: function (r) {
                    frappe.model.set_value(cdt, cdn, "employee_name", r.message);
                }
            });

        }
    },
    labour_fees: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "work_order_total", frappe.model.get_value(cdt, cdn, "materials_total") + frappe.model.get_value(cdt, cdn, "labour_fees") + frappe.model.get_value(cdt, cdn, "transport_fare"));

    },

    transport_fare: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "work_order_total", frappe.model.get_value(cdt, cdn, "materials_total") + frappe.model.get_value(cdt, cdn, "labour_fees") + frappe.model.get_value(cdt, cdn, "transport_fare"));
        frappe.model.set_value(cdt, cdn, "balance_due_upon_job_completion", frappe.model.get_value(cdt, cdn, "work_order_total") - frappe.model.get_value(cdt, cdn, "work_order_advance"));
    },

});

frappe.ui.form.on('Job Card Material Detail', {
    no_of_units: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "total", frappe.model.get_value(cdt, cdn, "no_of_units") * frappe.model.get_value(cdt, cdn, "unit_cost"));
    },
    unit_cost: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "total", frappe.model.get_value(cdt, cdn, "no_of_units") * frappe.model.get_value(cdt, cdn, "unit_cost"));
    }
});
