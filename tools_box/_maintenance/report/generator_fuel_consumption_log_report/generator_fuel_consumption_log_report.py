# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = [
		"Name:Link/Generator Fuel Consumption Log:100",
		"Date:Date:120",
		"Generator:Link/Asset:150",
		"Generator Name:Data:250",
		"Fuel Qty:Float:150",
		"Unit Price:Currency/currency;100",
		"Total Price:Currency/currency:100",
	]
	data, conditions = [], ""

	if filters.get('modified_from') and filters.get('modified_to'):
		conditions = " and p.date between DATE('{modified_from}') and DATE('{modified_to}')"

	if filters.get('generator'):
		conditions += " and p.generator = '{generator}'"

	data = frappe.db.sql("SELECT p.name , p.date, p.generator, p.generator_name, c.fuel_qty, c.unit_price, c.total "
							"FROM `tabGenerator Fuel Consumption Log` p JOIN `tabGenerator Fuel Consumption Log Item` c "
							"ON (p.name = c.parent) WHERE (1=1){conds}".format(conds=conditions.format(**filters)),
						 as_list=1)
	return columns, data
