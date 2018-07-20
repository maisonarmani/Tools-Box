// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext.hr");

erpnext.hr.RequisitionController = frappe.ui.form.Controller.extend({
	requisition_type: function(doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(!doc.company) {
			d.requisition_type = "";
			frappe.msgprint(__("Please set the Company"));
			this.frm.refresh_fields();
			return;
		}

		if(!d.requisition_type) {
		 	return;
		}

		return frappe.call({
			method: "tools_box._hr.doctype.requisition.requisition.get_requisition_account",
			args: {
				"req_type": d.requisition_type,
				"company": doc.company
			},
			callback: function(r) {
				if (r.message) {
					d.default_account = r.message.account;
				}
			}
		});
	}
});

$.extend(cur_frm.cscript, new erpnext.hr.RequisitionController({frm: cur_frm}));

cur_frm.add_fetch('employee', 'company', 'company');
cur_frm.add_fetch('employee','employee_name','employee_name');

cur_frm.cscript.onload = function(doc) {
	if(!doc.approval_status)
		cur_frm.set_value("approval_status", "Draft");

	if (doc.__islocal) {
		cur_frm.set_value("posting_date", frappe.datetime.get_today());
		if(doc.amended_from)
			cur_frm.set_value("approval_status", "Draft");
		cur_frm.cscript.clear_sanctioned(doc);
	}

	cur_frm.fields_dict.employee.get_query = function() {
		return {
			query: "erpnext.controllers.queries.employee_query"
		};
	};

	cur_frm.set_query("req_approver", function() {
		return {
			query: "tools_box._hr.doctype.requisition.requisition.get_expense_approver"
		};
	});
};

cur_frm.cscript.clear_sanctioned = function(doc) {
	var val = doc.requisition || [];
	for(var i = 0; i<val.length; i++){
		val[i].sanctioned_amount ='';
	}

	doc.total_sanctioned_amount = '';
	refresh_many(['sanctioned_amount', 'total_sanctioned_amount']);
};

cur_frm.cscript.refresh = function(doc) {
	cur_frm.cscript.set_help(doc);

	if(!doc.__islocal) {
		cur_frm.toggle_enable("req_approver", doc.approval_status=="Draft");
		cur_frm.toggle_enable("approval_status", (doc.req_approver==frappe.session.user && doc.docstatus==0));

		if (doc.docstatus==0 && doc.req_approver==frappe.session.user && doc.approval_status=="Approved")
			cur_frm.savesubmit();

		if (doc.docstatus===1 && doc.approval_status=="Approved") {
			/* eslint-disable */
			// no idea how `me` works here
			if (cint(doc.total_amount_reimbursed) > 0 && frappe.model.can_read("Journal Entry")) {
				cur_frm.add_custom_button(__('Bank Entries'), function() {
					frappe.route_options = {
						"Journal Entry Account.reference_type": me.frm.doc.doctype,
						"Journal Entry Account.reference_name": me.frm.doc.name,
						company: me.frm.doc.company
					};
					frappe.set_route("List", "Journal Entry");
				}, __("View"));
			}
			/* eslint-enable */
		}
	}
};

cur_frm.cscript.set_help = function(doc) {
	cur_frm.set_intro("");
	if(doc.__islocal && !in_list(frappe.user_roles, "HR User")) {
		cur_frm.set_intro(__("Fill the form and save it"));
	} else {
		if(doc.docstatus==0 && doc.approval_status=="Draft") {
			if(frappe.session.user==doc.req_approver) {
				cur_frm.set_intro(__("You are the Approver for this record. Please Update the 'Status' and Save"));
			} else {
				cur_frm.set_intro(__("Requisition is pending approval. Only the Requisition Approver can update status."));
			}
		}
	}
};

cur_frm.cscript.validate = function(doc) {
	cur_frm.cscript.calculate_total(doc);
};

cur_frm.cscript.calculate_total = function(doc){
	doc.total_requisition_amount = 0;
	doc.total_sanctioned_amount = 0;
	$.each((doc.expenses || []), function(i, d) {

		doc.total_requisition_amount += d.requisition_amount;
		doc.total_sanctioned_amount += d.sanctioned_amount;
	});

	refresh_field("total_claimed_amount");
	refresh_field('total_sanctioned_amount');
};

cur_frm.cscript.calculate_total_amount = function(doc,cdt,cdn){
	cur_frm.cscript.calculate_total(doc,cdt,cdn);
};

cur_frm.cscript.on_submit = function() {
	if(cint(frappe.boot.notification_settings && frappe.boot.notification_settings.expense_claim)) {
		cur_frm.email_doc(frappe.boot.notification_settings.expense_claim_message);
	}
};

erpnext.expense_claim = {
	set_title :function(frm) {
		if (!frm.doc.task) {
			frm.set_value("title", frm.doc.employee_name);
		}
		else {
			frm.set_value("title", frm.doc.employee_name + " for "+ frm.doc.task);
		}
	}
};

frappe.ui.form.on("Requisition", {
	setup: function(frm) {
		frm.trigger("set_query_for_cost_center");
		frm.trigger("set_query_for_receivable_account");
		frm.add_fetch("company", "cost_center", "cost_center");
		frm.add_fetch("company", "default_receivable_account", "receivable_account");
	},

	refresh: function(frm) {
		if(frm.doc.docstatus == 1 && frm.doc.approval_status == 'Approved') {
			frm.add_custom_button(__('Accounting Ledger'), function() {
				frappe.route_options = {
					voucher_no: frm.doc.name,
					company: frm.doc.company,
					group_by_voucher: false
				};
				frappe.set_route("query-report", "General Ledger");
			}, __("View"));
		}

		if (false){
			if (frm.doc.docstatus===1 && frm.doc.approval_status=="Approved" && frm.doc.workflow_state == "Paid"
					&& (cint(frm.doc.total_amount_reimbursed) < cint(frm.doc.total_sanctioned_amount))
					&& frappe.model.can_create("Payment Entry")) {
				frm.add_custom_button(__('Retirement'),
					function() { frm.events.make_retirement_entry(frm); }, __("Make"));
			}
		}
	},

	make_retirement_entry: function(frm) {
		var method = "erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry";
		if(frm.doc.__onload && frm.doc.__onload.make_payment_via_journal_entry) {
			method = "tools_box._hr.doctype.requisition.requisition.make_bank_entry"
		}
		return frappe.call({
			method: method,
			args: {
				"dt": frm.doc.doctype,
				"dn": frm.doc.name
			},
			callback: function(r) {
				var doclist = frappe.model.sync(r.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		});
	},

	set_query_for_cost_center: function(frm) {
		frm.fields_dict["cost_center"].get_query = function() {
			return {
				filters: {
					"company": frm.doc.company
				}
			};
		};
	},

	set_query_for_receivable_account: function(frm) {
		frm.fields_dict["receivable_account"].get_query = function() {
			return {
				filters: {
					"report_type": "Balance Sheet",
					"account_type": "Receivable"
				}
			};
		};
	},

	is_paid: function(frm) {
		frm.trigger("toggle_fields");
	},

	employee_name: function(frm) {
		erpnext.expense_claim.set_title(frm);
	},

	task: function(frm) {
		erpnext.expense_claim.set_title(frm);
	}
});

frappe.ui.form.on("Requisition Detail", {
	claim_amount: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		var doc = frm.doc;

		if(!child.sanctioned_amount){
			frappe.model.set_value(cdt, cdn, 'sanctioned_amount', child.claim_amount);
		}

		cur_frm.cscript.calculate_total(doc,cdt,cdn);
	},

	sanctioned_amount: function(frm, cdt, cdn) {
		var doc = frm.doc;
		cur_frm.cscript.calculate_total(doc,cdt,cdn);
	}
});

cur_frm.fields_dict['task'].get_query = function(doc) {
	return {
		filters:{
			'project': doc.project
		}
	};
};
