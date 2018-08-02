# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    columns = [
        "Posting Date:Date:100",
        "Employee:Link/Employee:100",
        "Employee Name:Data:150",
        "Advance Amount:Currency:120",
        "Paid Amount:Currency:120",
        "Retired Amount:Currency:130",
        "Refunded Amount:Currency:130",
        "Variance:Currency:120",
    ]


    conditions = ""
    if filters.get("from_date"):
        conditions += "d.posting_date >= DATE('{from_date}')"
    if filters.get("to_date"):
        conditions += " AND d.posting_date <= DATE('{to_date}')"

    if filters.get("status") and filters.get('status') != "Retired":
        conditions += " AND d.status = '{status}'"
    else:
        conditions += " AND d.claimed_amount = d.advance_amount or  AND d.refunded = d.advance_amount "


    data = frappe.db.sql("SELECT d.posting_date, d.employee, d.employee_name , d.advance_amount, d.paid_amount, "
                         "d.claimed_amount, d.refund_amount, (d.refund_amount + d.claimed_amount - d.paid_amount) FROM "
                         "`tabEmployee Advance` d WHERE {0} ".format(conditions.format(**filters)), as_list=1)

    return columns, data
