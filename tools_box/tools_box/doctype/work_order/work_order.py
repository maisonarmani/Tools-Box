# -*- coding: utf-8 -*-
# Copyright (c) 2018, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class WorkOrder(Document):
    pass


@frappe.whitelist()
def get_requested_by(ticket_number):
    ticket = frappe.get_doc("Equipment Support", ticket_number)
    employee = frappe.get_doc("Employee", ticket.raised_by)

    return employee.name


@frappe.whitelist()
def get_employee_name(ticket_number):
    ticket = frappe.get_doc("Equipment Support", ticket_number)
    employee = frappe.get_doc("Employee", ticket.raised_by)

    return employee.employee_name




@frappe.whitelist()
def make_purchase_order(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.ignore_pricing_rule = 1
        target.run_method("set_missing_values")
        target.run_method("get_schedule_dates")
        target.run_method("calculate_taxes_and_totals")

    target_doc = get_mapped_doc("Work Order", source_name, {
        "Job Card": {
            "doctype": "Purchase Order",
            "field_map": {
                "vendor": "supplier",
                "date": "transaction_date",
                "name": "work_order"
            }
        },
        "Job Card Material Detail": {
            "doctype": "Purchase Order Item",
            "field_map": {
                "item_code": "item_code",
                "item_name": "item_name",
                "item_description": "description",
                "uom": "stock_uom",
                "no_of_units": "qty",
                "unit_cost": "rate",
                "conversion_factor": 1,
                "total": "amount"
            }
        }
    }, target_doc, set_missing_values)

    return target_doc
