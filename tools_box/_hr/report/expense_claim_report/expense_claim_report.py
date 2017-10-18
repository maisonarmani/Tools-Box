# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    if not filters: filters = {}
    columns = ["Date:Date:100", "Doc ID:Link/Expense Claim:150", "Expense Claim Type:Link/Expense Claim Type:100",
               "Description:Text:200", "Amount:Currency:120", "Cost Center:Link/Cost Center:130", "Approver:Link/User:200"]
    conditions, include_auth, comment_by = "", "", ""
    if filters.get("from_date"):
        conditions += " AND d.expense_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND d.expense_date <= %(to_date)s"
    if filters.get("approver"):
        conditions += " AND p.exp_approver = %(approver)s"
    if filters.get("expense_type"):
        conditions += " AND d.expense_type = %(expense_type)s"
    if filters.get("cost_center"):
        conditions += " AND p.cost_center = %(cost_center)s"
    if filters.get("include_authorized"):
        comment_by = ",  c.comment_by"
        columns += [ "Authorized:Link/User:200"]
        include_auth = "LEFT OUTER JOIN tabComment c ON (p.name = c.comment_docname) and c.comment = 'Authorized'"

    data = frappe.db.sql(
        "SELECT d.expense_date,p.name,d.expense_type,d.description,d.sanctioned_amount,p.cost_center,p.exp_approver {0} FROM "
        "`tabExpense Claim` p LEFT JOIN `tabExpense Claim Detail` d ON (p.name = d.parent) {1} WHERE p.docstatus=1 {2}"
            .format(comment_by, include_auth, conditions), filters)

    return columns, data
