# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from erpnext import get_default_company


class OvertimeSheet(Document):
    def validate(self):
        overtime_sheet = frappe.db.sql("""select name from `tabOvertime Sheet` where overtime=%s and name != %s"""
                            % (self.overtime_request, self.name))
        if overtime_sheet:
            frappe.throw("Sorry, Overtime Request %s is already in use." % self.overtime_request)



@frappe.whitelist()
def make_expense_claim_new(docname):
    def check_exp_claim_exists():
        exp = frappe.db.sql("""select name from `tabExpense Claim` where overtime=%s""", overtime.name)
        return exp[0][0] if exp else ""

    overtime = frappe.get_doc("Overtime Sheet", docname)
    exp_claim = check_exp_claim_exists()
    if exp_claim:
        frappe.throw(_("Expense Claim {0} already exists for the Overtime sheet").format(exp_claim))

    total = 0
    for i in overtime.overtime_information:
        total += i.amount

    exp_claim = frappe.new_doc("Expense Claim")
    exp_claim.employee = overtime.raised_by
    exp_claim.overtime = overtime.name
    exp_claim.remark = _("Overtime payment for {0} between {1} and {2}").format(overtime.name, overtime.start_time,
                                                                                overtime.end_time)
    exp_claim.append("expenses", {
        "expense_date": overtime.date,
        "description": _("Overtime payment for {0} between {1} and {2}").format(overtime.name, overtime.start_time,
                                                                                overtime.end_time),
        "expense_type": "Overtime",
        "claim_amount": total,
        "sanctioned_amount": total
    })
    return exp_claim.as_dict()


def make_expense_claim(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.employee = source.raise_by
        target.remark = "Overtime payment for {0} between {1} and {2}".format(source.name, source.start_time,
                                                                              source.end_time)
        target.ignore_pricing_rule = 1
        target.run_method("set_missing_values")
        target.run_method("calculate_taxes_and_totals")

        # set company
        target.update({"company": get_default_company()})

    def update_item(source, target, source_parent):
        target.sanctioned_amount = source_parent.total
        target.claimed_amount = source_parent.total
        target.description = source_parent.total
        target.expense_type = "Overtime payment for {0} between {1} and {2}".format(source.name, source.start_time,
                                                                                    source.end_time)
        target.expense_date = source_parent.date

    target_doc = get_mapped_doc("Overtime Sheet", source_name, {
        "Overtime Sheet": {
            "doctype": "Expense Claim",
            "validation": {
                "docstatus": ["=", 0]
            }
        },
        "Overtime Sheet Item": {
            "doctype": "Delivery Note Item",
            "field_map": {},
            "postprocess": update_item,
        }
    }, target_doc, set_missing_values)

    return target_doc
