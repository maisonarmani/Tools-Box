# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	data, conditions = [], ""
	columns = [
		"Date:Date:100",
		"Vehicle:Link/Vehicle:100",
	]


	data = frappe.db.sql("""select p.date, p.vehicle from `tabVehicle Schedule` p RIGHT OUTER JOIN 
							(`tabVehicle Schedule Outbound Item` c1 JOIN  `tabVehicle Schedule Inbound Item` c2 ) 
							ON (p.name=c1.parent) and (p.name=c2.parent)""")

	return columns,data

