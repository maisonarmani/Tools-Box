# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	data, conditions = [], ""
	columns = [
		"Date:Date:100",
		"Vehicle:Link/Vehicle:100",
		"Type:Data:100",
		"Remark:Data:120",
		"Reason:Data:120",
		"Ref Type:Link/Doctype:120",
		"Ref Name:Data:130",
		"Status:Data:130",
		"Amount:Currency:130"
	]

	if filters.get('from') and filters.get('to'):
		conditions += " and date BETWEEN DATE('{from}') and DATE('{to}')"

	if filters.get('vehicle'):
		conditions += " and vehicle = '{vehicle}'"

	if filters.get('type') :
		conditions += " and type = '{type}'"

	schedules = frappe.db.sql("""select type from `tabVehicle Schedule` where (1=1) {cond} """
							  .format(cond = conditions.format(**filters)), as_dict=1)

	for schedule in schedules:
		data.extend(list(__get_bound(schedule.type))[0:])

	return columns,data


def __get_bound(type = None):
		items = frappe.db.sql("""select p.date, p.vehicle, p.type, p.remark, p.reason, c.ref_type, c.ref_name,
		 c.status, c.amount from `tabVehicle Schedule` as p LEFT OUTER JOIN `tabVehicle Schedule {type} Item` as c ON(c.parent = p.name)"""
								.format(type=type))
		return items



