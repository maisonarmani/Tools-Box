// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
cur_frm.add_fetch('item_code', 'stock_uom', 'uom');
cur_frm.add_fetch('item_code', 'item_name', 'item_name');
cur_frm.add_fetch('item_code', 'description', 'item_description');
cur_frm.set_query("approver", function () {
    return {
        query: "erpnext.hr.doctype.expense_claim.expense_claim.get_expense_approver"
    };
});
frappe.ui.form.on('Job Card', {
    refresh: function (frm) {
        if (cur_frm.doc.status == 'Approved') {
            cur_frm.add_custom_button('Make Purchase Order', function () {
                frappe.model.open_mapped_doc({
                    method: "graceco_tools.graceco_tools.doctype.job_card.job_card.make_purchase_order",
                    frm: cur_frm
                });
                /*                var po = frappe.model.make_new_doc_and_get_name('Purchase Order');
                 po = locals['Purchase Order'][po];
                 po.supplier = cur_frm.doc.vendor;
                 po.buying_price_list = 'Standard Buying';
                 var material = cur_frm.doc.job_card_material_detail || [];
                 for(var i = 0; i < material.length; i++){
                 var d1 = frappe.model.add_child(po, 'Purchase Order Item', 'items');
                 d1.item_code = material[i].item_code;
                 d1.item_name = material[i].item_name;
                 d1.qty = material[i].no_of_units;
                 d1.uom = material[i].uom;
                 d1.stock_uom = material[i].uom;
                 d1.description = material[i].item_description;
                 d1.rate = material[i].unit_cost;
                 d1.schedule_date = cur_frm.doc.proposed_completion_date;
                 }
                 frappe.route_options = {"supplier":cur_frm.doc.vendor,"buying_price_list":'Standard Buying',"transaction_date":cur_frm.doc.job_card_date};
                 frappe.set_route("Form",'Purchase Order', po.name);
                 //loaddoc('Purchase Order', po.name);
                 */
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
            //cur_frm.set_df_property('status','read_only',0);
            cur_frm.set_df_property('approval', 'read_only', 0);
        }
        cur_frm.set_df_property('status', 'read_only', 1);

    },

    ticket_number: function (frm, cdt, cdn) {
        var job_card = frappe.model.get_doc(cdt, cdn);
        if (job_card.ticket_number) {
            frappe.call({
                method: "graceco_tools.graceco_tools.doctype.job_card.job_card.get_requested_by",
                args: {
                    ticket_number: job_card.ticket_number
                },
                callback: function (r) {

                    frappe.model.set_value(cdt, cdn, "requested_by", r.message);
                }
            });
            frappe.call({
                method: "graceco_tools.graceco_tools.doctype.job_card.job_card.get_employee_name",
                args: {
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
    /*
     item_code: function(frm, cdt, cdn) {
     var job_card_material_detail = frappe.model.get_doc(cdt, cdn);
     if (job_card_material_detail.item_code) {
     frappe.call({
     method: "erpnext.support.doctype.job_card.job_card.get_item_name",
     args: {
     item_code: job_card_material_detail.item_code
     },
     callback: function(r) {

     frappe.model.set_value(cdt, cdn, "item_name", r.message);
     }
     });

     frappe.call({
     method: "erpnext.support.doctype.job_card.job_card.get_item_description",
     args: {
     item_code: job_card_material_detail.item_code
     },
     callback: function(r) {

     frappe.model.set_value(cdt, cdn, "item_description", r.message);
     }
     });

     }
     },
     */
    no_of_units: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "total", frappe.model.get_value(cdt, cdn, "no_of_units") * frappe.model.get_value(cdt, cdn, "unit_cost"));
    },

    unit_cost: function (frm, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, "total", frappe.model.get_value(cdt, cdn, "no_of_units") * frappe.model.get_value(cdt, cdn, "unit_cost"));

    },

});
