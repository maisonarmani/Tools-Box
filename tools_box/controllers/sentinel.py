# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

def validate_status(document,trigger):
    sanitized = ["Sales Order","Purchase Order","Expense Claim"]
    for doc in sanitized:
        frappe.db.sql("update `tab{}` set workflow_state = \"Draft\" where workflow_state = 'Approved' and docstatus = 0 "
                      .format(doc))