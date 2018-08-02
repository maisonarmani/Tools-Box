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
frappe.ui.form.on('Job Card', {
    onload: function (frm) {
        if (cur_frm.doc.asset_category != "Plant and Machinery")
            cur_frm.toggle_reqd("ticket_number", true)
        frm.set_query("requested_by", get_employees);
        frappe.model.set_value(frm.doctype,frm.docname, 'requested_by',frm.doc.requested_by);

    },
    asset_category: function (frm) {
        cur_frm.toggle_reqd("ticket_number", false);
        if (cur_frm.doc.asset_category != "Plant and Machinery")
            cur_frm.toggle_reqd("ticket_number", true);

        cur_frm.set_query("asset", function () {
            return {
                "filters": {
                    "asset_category": cur_frm.doc.asset_category
                }
            };
        });
    },
    refresh: function (frm) {
        if (cur_frm.doc.asset_category != "Plant and Machinery")
            cur_frm.toggle_reqd("ticket_number", true)
        frm.set_query("job_completion_verified_by", get_employees);
        frm.set_query("requested_by", get_employees);
        if (cur_frm.doc.status == 'Not Completed') {
            cur_frm.add_custom_button('Make Purchase Order', function () {
                frappe.model.open_mapped_doc({
                    method: "tools_box.tools_box.doctype.job_card.job_card.make_purchase_order",
                    frm: cur_frm
                });
            });
        }

        if ((cur_frm.doc.equipment_maintenance_log || !cur_frm.doc.vendor) &&
            in_list(['Not Completed', 'IAD Cleared'], cur_frm.doc.status)) {
            cur_frm.add_custom_button('Make Expense Claim', function () {
                frappe.model.open_mapped_doc({
                    method: "tools_box.tools_box.doctype.job_card.job_card.make_expense_claim",
                    frm: cur_frm
                });
            });
            cur_frm.add_custom_button('Make Employee Advance', function () {
                frappe.model.open_mapped_doc({
                    method: "tools_box.tools_box.doctype.job_card.job_card.make_employee_advance",
                    frm: cur_frm
                });
            });
        }

        if (!frappe.user.has_role(['Helpdesk Admin'])) {
            cur_frm.fields.forEach(function (l) {
                cur_frm.set_df_property(l.df.fieldname, "read_only", (cur_frm.doc.status == 'Approved' || cur_frm.doc.status == 'Completed'));
            })
        }
        else {
            cur_frm.fields.forEach(function (l) {
                cur_frm.set_df_property(l.df.fieldname, "read_only", (cur_frm.doc.status == 'Approved' || cur_frm.doc.status == 'Completed'));
            })
            cur_frm.set_df_property('job_completion_date', 'read_only', 0);
            cur_frm.set_df_property('job_completion_verified_by', 'read_only', 0);
            cur_frm.set_df_property('approval', 'read_only', 0);
        }

        cur_frm.set_df_property('status', 'read_only', 1);

    },
    ticket_number: function (frm, cdt, cdn) {
        var job_card = frappe.model.get_doc(cdt, cdn);
        if (job_card.ticket_number) {
            frappe.call({
                method: "tools_box.tools_box.doctype.job_card.job_card.get_requested_by",
                args: {
                    ticket_type:job_card.ticket_type,
                    ticket_number: job_card.ticket_number
                },
                callback: function (r) {
                    frappe.model.set_value(cdt, cdn, "requested_by", r.message);
                }
            });
            frappe.call({
                method: "tools_box.tools_box.doctype.job_card.job_card.get_employee_name",
                args: {
                    ticket_type:job_card.ticket_type,
                    ticket_number: job_card.ticket_number
                },
                callback: function (r) {
                    frappe.model.set_value(cdt, cdn, "employee_name", r.message);
                }
            });

        }
    },

    job_advance: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "balance_due_upon_job_completion", frappe.model.get_value(cdt, cdn, "job_card_total") - frappe.model.get_value(cdt, cdn, "job_advance"));
    },

    labour_fees: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "job_card_total", frappe.model.get_value(cdt, cdn, "materials_total") + frappe.model.get_value(cdt, cdn, "labour_fees") + frappe.model.get_value(cdt, cdn, "transport_fare"));
        frappe.model.set_value(cdt, cdn, "balance_due_upon_job_completion", frappe.model.get_value(cdt, cdn, "job_card_total") - frappe.model.get_value(cdt, cdn, "job_advance"));
    },

    transport_fare: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "job_card_total", frappe.model.get_value(cdt, cdn, "materials_total") + frappe.model.get_value(cdt, cdn, "labour_fees") + frappe.model.get_value(cdt, cdn, "transport_fare"));
        frappe.model.set_value(cdt, cdn, "balance_due_upon_job_completion", frappe.model.get_value(cdt, cdn, "job_card_total") - frappe.model.get_value(cdt, cdn, "job_advance"));
    },

});

frappe.ui.form.on('Job Card Material Detail', {
    no_of_units: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "total", frappe.model.get_value(cdt, cdn, "no_of_units") * frappe.model.get_value(cdt, cdn, "unit_cost"));
        recalculate_total(frm.doctype,frm.docname)
    },
    unit_cost: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "total", frappe.model.get_value(cdt, cdn, "no_of_units") * frappe.model.get_value(cdt, cdn, "unit_cost"));
        recalculate_total(frm.doctype,frm.docname)

    }
});

function recalculate_total(cdt,cdn){
        var _total = 0;
        cur_frm.doc.job_card_material_detail.forEach(function(v){ _total += v.total; });
        frappe.model.set_value(cdt, cdn, "job_card_total", frappe.model.get_value(cdt, cdn, "job_card_total") +  _total);
        frappe.model.set_value(cdt, cdn, "balance_due_upon_job_completion", frappe.model.get_value(cdt, cdn, "job_card_total") - frappe.model.get_value(cdt, cdn, "job_advance"));
}
