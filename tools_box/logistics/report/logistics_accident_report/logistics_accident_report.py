# Copyright (c) 2018, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	data, conditions = [], ""
	columns = [
		"Date:Date:100",
		"Vehicle:Link/Vehicle:100",
		"Type:Data:100",
		"Description:Data:100",
		"Driver:Link/Driver:120",
		"Location:Data:120",
		"Resolution:Data:120",
		"Total Cost:Currency:120"
	]

	if filters.get('from') and filters.get('to'):
		conditions += " and date BETWEEN DATE('{from}') and DATE('{to}')"

	if filters.get('vehicle'):
		conditions += " and vehicle = '{vehicle}'"

	if filters.get('type') :
		conditions += " and driver = '{driver}'"

	data = frappe.db.sql("""select p.date, p.vehicle, p.type, p.description, p.driver,p.location, p.resolution, p.total_cost 
							from `tabLogistics Accident` p where (1=1) {cond} """
						 .format(cond = conditions.format(**filters)))

	return columns,data

