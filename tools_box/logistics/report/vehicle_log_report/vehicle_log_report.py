# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe

def execute(filters={}):
	columns = [
		"ID:Link/Vehicle Log:150",
		"Date:Date:150",
		"Vehicle:Link/Vehicle:130",
		"Model/Make:Data:120",
		"Employee:Data:150",
		"Fuel Qty:Float:100",
		"Fuel Price:Currency:100",
		"Total:Currency:100",
	]
	conditions = ""
	if filters.get("from_date"):
		conditions += " AND vl.date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND vl.date <= %(to_date)s"
	if filters.get("vehicle"):
		conditions += " AND vl.license_plate = %(vehicle)s"
	if filters.get("driver"):
		conditions += " AND vl.employee = %(employee)s"
	data = frappe.db.sql("select vl.name , vl.date, vl.license_plate, CONCAT(vl.model,'-' ,vl.make) car, "
						 "emp.employee_name, vl.fuel_qty, vl.price , (vl.fuel_qty * vl.price) total from "
						 "`tabVehicle Log` vl LEFT OUTER JOIN `tabEmployee` emp ON(emp.name=vl.employee) where "
						 " (1=1) {0}".format(conditions), filters)
	return columns, data
