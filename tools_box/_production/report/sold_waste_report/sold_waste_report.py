# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data, conditions = [], [], ""
	columns = [
		"Date:Date:100",
		"Waste Officer:Link/Employee:100",
		"Waste Offficer Name:Data:180",
		"Item:Link/Item:100",
		"Item Name:Data:170",
		"UOM:Data:50",
		"Amount:Currency:120"
	]

	if filters.get('from') and filters.get('to'):
		conditions += " and p.date BETWEEN DATE('{from}') and DATE('{to}')"

	if filters.get('status'):
		conditions += " and p.status = '{status}'"
		if filters.get('status') == "Sold":
			conditions += " and p.docstatus = 1"

	if filters.get('item'):
		conditions += " and c.item = '{item}'"


	data = frappe.db.sql("""select p.date,p.waste_officer, p.waste_officer_name, c.item, c.item_name, c.uom, c.amount 
					from `tabSold Waste` p JOIN  `tabSold Waste Item` c ON(p.name =c.parent) WHERE (1=1) {cond}""".
						 format(cond=conditions.format(**filters)))

	return columns, data
