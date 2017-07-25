# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe

def execute(filters={}):
	columns = [
		"Name:Link/Sales Weekly Report:150",
		"Report From:Date:150",
		"Report To:Date:150",
		"Sales Person:Link/Sales Person:130",
		"Achievement:Float:130",
		"Visited:Float:130",
		"New Outlet Visited:Float:130",
	]
	conditions = ""
	if filters.get("report_from"):
		conditions += " AND report_from >= %(report_from)s"
	if filters.get("report_to"):
		conditions += " AND report_to <= %(report_to)s"
	if filters.get("sales_person"):
		conditions += " AND sales_person = %(sales_person)s"

	data = frappe.db.sql("select name,report_from,report_to,sales_person, per_achievement,visited,new_outlets_visited"
						 " from `tabSales Weekly Report` where (1=1) {0}".format(conditions), filters)
	return columns, data
