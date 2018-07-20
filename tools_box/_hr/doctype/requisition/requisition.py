# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import get_fullname, flt, cstr
from frappe.model.document import Document
from erpnext.hr.utils import set_employee_name
from erpnext.accounts.party import get_party_account
from erpnext.accounts.general_ledger import make_gl_entries
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
from erpnext.controllers.accounts_controller import AccountsController
from frappe.utils.csvutils import getlink


class InvalidRequisitionApproverError(frappe.ValidationError): pass


class Requisition(AccountsController):
    def onload(self):
        self.get("__onload").make_payment_via_journal_entry = frappe.db.get_single_value('Accounts Settings',
                                                                                         'make_payment_via_journal_entry')

    def get_feed(self):
        return _("{0}: From {0} for {1}").format(self.approval_status,
                                                 self.employee_name, self.total_requisition_amount)

    def validate(self):
        self.validate_sanctioned_amount()
        self.validate_requisition_approver()
        self.calculate_total_amount()
        set_employee_name(self)
        self.set_requisition_account()
        self.set_receivable_account()
        self.set_cost_center()
        self.set_status()
        if self.task and not self.project:
            self.project = frappe.db.get_value("Task", self.task, "project")

    def set_status(self):
        self.status = {
            "0": "Draft",
            "1": "Submitted",
            "2": "Cancelled"
        }[cstr(self.docstatus or 0)]

        if self.total_sanctioned_amount > 0 and self.total_sanctioned_amount == self.total_amount_retired \
                and self.docstatus == 1 and self.approval_status == 'Approved':
            self.status = "Retired"
        elif self.total_sanctioned_amount > 0 and self.docstatus == 1 and self.approval_status == 'Approved':
            self.status = "Unpaid"
        elif self.docstatus == 1 and self.approval_status == 'Rejected':
            self.status = 'Rejected'

    def set_receivable_account(self):
        if not self.receivable_account :
            self.receivable_account = frappe.db.get_value("Company", self.company, "default_receivable_account")

    def set_cost_center(self):
        if not self.cost_center:
            self.cost_center = frappe.db.get_value('Company', self.company, 'cost_center')

    def on_submit(self):
        if self.approval_status == "Draft":
            frappe.throw(_("""Approval Status must be 'Approved' or 'Rejected'"""))

        self.update_task_and_project()
        self.set_status()


    def pay(self):
        gl_entry = []
        self.validate_account_details()

        # payment entry
        payment_account = get_bank_cash_account(self.mode_of_payment, self.company).get("account")
        gl_entry.append(
            self.get_gl_dict({
                "account": payment_account,
                "credit": self.total_sanctioned_amount,
                "credit_in_account_currency": self.total_sanctioned_amount,
                "against": self.employee
            })
        )

        # payable entry
        gl_entry.append(
            self.get_gl_dict({
                "account": self.receivable_account,
                "debit": self.total_sanctioned_amount,
                "debit_in_account_currency": self.total_sanctioned_amount,
                "against": ",".join([d.default_account for d in self.requisition]),
                "party_type": "Employee",
                "party": self.employee,
                "against_voucher_type": self.doctype,
                "against_voucher": self.name
            })
        )

        if flt(self.total_sanctioned_amount) > 0:
            make_gl_entries(gl_entry, False)

    def retire(self):
        gl_entry = []

        payment_account = get_bank_cash_account(self.mode_of_payment, self.company).get("account")
        # expense entries
        for data in self.requisition:
            gl_entry.append(
                self.get_gl_dict({
                    "account": data.default_account,
                    "debit": data.sanctioned_amount,
                    "debit_in_account_currency": data.sanctioned_amount,
                    "against": self.employee,
                    "cost_center": self.cost_center
                })
            )

        gl_entry.append(
            self.get_gl_dict({
                "account": self.receivable_account,
                "party_type": "Employee",
                "party": self.employee,
                "against": payment_account,
                "credit": self.total_sanctioned_amount,
                "credit_in_account_currency": self.total_sanctioned_amount,
                "against_voucher": self.name,
                "against_voucher_type": self.doctype,
            })
        )


        if flt(self.total_sanctioned_amount) > 0:
            make_gl_entries(gl_entry, False)

        update_retired_amount(self)

    def on_change(self):
        if self.workflow_state == "Retired":
            if not self.mode_of_payment:
                frappe.throw(_("""Mode of payment must be set"""))
            self.retire()

        if self.workflow_state == "Paid":
            if not self.mode_of_payment:
                frappe.throw(_("""Mode of payment must be set"""))
            self.pay()

    def on_cancel(self):
        self.update_task_and_project()
        if self.receivable_account:
            self.make_gl_entries(cancel=True)

        self.set_status()

    def update_task_and_project(self):
        if self.task:
            self.update_task()
        elif self.project:
            frappe.get_doc("Project", self.project).update_project()


    def validate_account_details(self):
        if not self.cost_center:
            frappe.throw(_("Cost center is required to book an requisition"))

        if not self.receivable_account:
            frappe.throw(
                _("Please set default receivable account for the company {0}").format(getlink("Company", self.company)))

        if not self.mode_of_payment:
            frappe.throw(_("Mode of payment is required to make a payment").format(self.employee))

    def calculate_total_amount(self):
        self.total_requisition_amount = 0
        self.total_sanctioned_amount = 0
        for d in self.get('requisition'):
            if self.approval_status == 'Rejected':
                d.sanctioned_amount = 0.0

            self.total_requisition_amount += flt(d.requisition_amount)
            self.total_sanctioned_amount += flt(d.sanctioned_amount)

    def validate_requisition_approver(self):
        if self.req_approver and "Expense Approver" not in frappe.get_roles(self.req_approver):
            frappe.throw(_("{0} ({1}) must have role 'Requisition Approver'") \
                         .format(get_fullname(self.req_approver), self.req_approver), InvalidRequisitionApproverError)

    def update_task(self):
        task = frappe.get_doc("Task", self.task)
        task.update_total_requisition()
        task.save()

    def validate_sanctioned_amount(self):
        for d in self.get('requisition'):
            if flt(d.sanctioned_amount) > flt(d.requisition_amount):
                frappe.throw(_("Sanctioned Amount cannot be greater than Requisition Amount in Row {0}.").format(d.idx))

    def set_requisition_account(self):
        for req in self.requisition:
            if not req.default_account:
                req.default_account = get_requisition_account(req.requisition_type, self.company)["account"]


def update_retired_amount(doc):
    amt = frappe.db.sql("""select ifnull(sum(credit_in_account_currency), 0) as amt 
		from `tabGL Entry` where against_voucher_type = 'Requisition' and against_voucher = %s
		and party = %s """, (doc.name, doc.employee), as_dict=1)[0].amt

    doc.total_amount_retired = amt
    frappe.db.set_value('Requisition', doc.name, "total_amount_retired", amt)

    doc.set_status()
    frappe.db.set_value('Requisition', doc.name, "status", doc.status)


@frappe.whitelist()
def get_expense_approver(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
		select u.name, concat(u.first_name, ' ', u.last_name)
		from tabUser u, `tabHas Role` r
		where u.name = r.parent and r.role = 'Expense Approver' 
		and u.enabled = 1 and u.name like %s
	""", ("%" + txt + "%"))


@frappe.whitelist()
def make_bank_entry(dt, dn):
    from erpnext.accounts.doctype.journal_entry.journal_entry import get_default_bank_cash_account

    requisition = frappe.get_doc(dt, dn)
    default_bank_cash_account = get_default_bank_cash_account(requisition.company, "Bank")
    if not default_bank_cash_account:
        default_bank_cash_account = get_default_bank_cash_account(requisition.company, "Cash")

    je = frappe.new_doc("Journal Entry")
    je.voucher_type = 'Bank Entry'
    je.company = requisition.company
    je.remark = 'Payment against Requisition: ' + dn;

    je.append("accounts", {
        "account": requisition.receivable_account,
        "debit_in_account_currency": flt(requisition.total_sanctioned_amount - requisition.total_amount_retired),
        "reference_type": dt,
        "party_type": "Employee",
        "party": requisition.employee,
        "reference_name": requisition.name
    })

    je.append("accounts", {
        "account": default_bank_cash_account.account,
        "credit_in_account_currency": flt(
            requisition.total_sanctioned_amount - requisition.total_amount_retired),
        "reference_type": "Expense Claim",
        "reference_name": requisition.name,
        "balance": default_bank_cash_account.balance,
        "account_currency": default_bank_cash_account.account_currency,
        "account_type": default_bank_cash_account.account_type
    })

    return je.as_dict()


@frappe.whitelist()
def get_requisition_account(req_type, company):
    account = frappe.db.get_value("Expense Claim Account",
                                  {"parent": req_type, "company": company}, "default_account")

    if not account:
        frappe.throw(_("Please set default account in Requisition Type {0}")
                     .format(req_type))

    return {
        "account": account
    }