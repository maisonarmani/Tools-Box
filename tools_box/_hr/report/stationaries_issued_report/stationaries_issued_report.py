# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    columns, data = ["Issued Date:Date:100", "Item:Link/Item:100", "Issued By:Link/Employee:150",
                     "Received By:Link/Employee:150", "Department:100", "Piece(s):Data:100"], []

    conditions = ""

    if filters.get('from') and filters.get('to'):
        conditions += " and p.issued_date BETWEEN DATE('{from}') and DATE('{to}')"

    if filters.get("item"):
        conditions += " and c.item_issued = {item}"

    if filters.get("department"):
        conditions += " and c.department = {department}"

    data = frappe.db.sql(
        "SELECT c.issued_date , c.item_issued, c.issued_by_name, c.received_by_name , c.department, c.pieces from "
        "`tabStationaries Issued` p JOIN  `tabStationaries Issued Items` c "
        "ON (p.name= c.parent) where (1=1) {cond}".format(cond=conditions.format(**filters)))

    return columns, data
