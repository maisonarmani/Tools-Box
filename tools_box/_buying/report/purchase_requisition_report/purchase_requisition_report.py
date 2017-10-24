# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    data, conditions = [], ""
    columns = [
        "Date:Date:100",
        "Requested By:Link/Employee:100",
        _("Amount")+":Currency:100"
    ]

    if filters.get('from') and filters.get('to'):
        conditions += " and date BETWEEN DATE('{from}') and DATE('{to}')"

    if filters.get('budgeted'):
        conditions += " and budgeted_expense= {budgeted}"

    data = frappe.db.sql("""select date, requested_by , total from `tabPurchase Requisition` 
					where (1=1) {cond} """.format(cond=conditions.format(**filters)))

    return columns, data
