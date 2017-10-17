# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    columns, data = ["Item:Link/Item:100", "Item Group:Link/Item Group:120", "Required Date:Date:140", "Warehouse:Link/Warehouse:150",
                     "Requested Quantity:Float:120","Actual Quantity:Float:120","Status:Data:100"], []

    conditions = ""

    if filters.get('from') and filters.get('to'):
        conditions += " and c.schedule_date BETWEEN DATE('{from}') and DATE('{to}')"

    if filters.get("item"):
        conditions += " and c.item_code = {item}"

    if filters.get("item_group"):
        conditions += " and c.item_group = {item_group}"

    if filters.get("status"):
        conditions += " and p.status = {status}"

    data = frappe.db.sql(
        "SELECT c.item_code, c.item_group, c.schedule_date, c.warehouse,c.qty, c.actual_qty , p.status from `tabMaterial Request` p"
		" JOIN  `tabMaterial Request Item` c ON (p.name= c.parent) where (1=1) {cond} and p.material_request_type='Purchase'"
			.format(cond=conditions.format(**filters)))

    return columns, data
