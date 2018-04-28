// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
var get_employees = function () {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}

cur_frm.add_fetch("assigned_to", "employee_name", "assigned_to_name");//,"employee_name")
cur_frm.cscript.add_buttons = function (frm) {
    if (cur_frm.doc.status != "Close" && in_list([cur_frm.doc.owner, "Administrator"], frappe.user.name)) {
        cur_frm.add_custom_button("Close Ticket", function () {
            frappe.call({
                method: "tools_box.tools_box.doctype.helpdesk_ticket.helpdesk_ticket.close_ticket",
                args: {
                    ticket_no: cur_frm.doc.name
                },
                callback: function (r) {
                    cur_frm.reload_doc()
                }
            });
        })
    }


    cur_frm.add_custom_button('Make Job Card', function () {
        var jc = frappe.model.make_new_doc_and_get_name('Job Card');
        jc = locals['Job Card'][jc];
        jc.ticket_number = cur_frm.doc.name;
        jc.priority = cur_frm.doc.priority;
        jc.asset = cur_frm.doc.asset;
        jc.asset_category = cur_frm.doc.asset_category;
	jc.requested_by = cur_frm.doc.raised_by;
	jc.employee_name = cur_frm.doc.raised_by_name;
        frappe.set_route("Form", "Job Card", jc.name);
    });

}
frappe.ui.form.on('Helpdesk Ticket', {
    onload: function (frm) {
        frm.set_query("raised_by", get_employees);
        frm.set_query("assigned_to", get_employees);

    },
    refresh: function (frm) {
        var assigned_on_hold_close = (cur_frm.doc.status == "Assigned" || cur_frm.doc.status == "On-Hold" || cur_frm.doc.status == "Close");
        cur_frm.set_df_property("priority", "read_only", assigned_on_hold_close);
        cur_frm.set_df_property("request_type", "read_only", assigned_on_hold_close);
        cur_frm.set_df_property("equipment", "read_only", assigned_on_hold_close);
        cur_frm.set_df_property("subject", "read_only", assigned_on_hold_close);
        cur_frm.set_df_property("raised_by", "read_only", assigned_on_hold_close);
        cur_frm.set_df_property("description", "read_only", assigned_on_hold_close);

        frm.cscript.add_buttons(frm);

        if (!frappe.user.has_role(['Helpdesk Admin'])) {
            cur_frm.set_df_property("status", "read_only", assigned_on_hold_close);
            cur_frm.set_df_property("first_responded_on", "read_only", assigned_on_hold_close);
            cur_frm.set_df_property("assigned_to", "read_only", assigned_on_hold_close);
            cur_frm.set_df_property("tech_administrator", "read_only", assigned_on_hold_close);
            cur_frm.set_df_property("contact", "read_only", assigned_on_hold_close);
            cur_frm.set_df_property("resolution", "read_only", assigned_on_hold_close);
            cur_frm.set_df_property("resolution_details", "read_only", assigned_on_hold_close);
        }
    },

    asset_category: function () {
        cur_frm.set_query("asset", function () {
            return {
                "filters": {
                    "asset_category": cur_frm.doc.asset_category
                }
            };
        });
    },

    raised_by: function (frm, cdt, cdn) {
        var ticket = frappe.model.get_doc(cdt, cdn);
        if (ticket.raised_by) {
            frappe.call({
                method: "tools_box.tools_box.doctype.helpdesk_ticket.helpdesk_ticket.get_full_name",
                args: {
                    raised_by: ticket.raised_by
                },
                callback: function (r) {
                    frappe.model.set_value(cdt, cdn, "raised_by_name", r.message);
                }
            });
        }
    },
});
