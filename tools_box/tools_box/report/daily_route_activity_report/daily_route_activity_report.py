# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if not filters: filters ={}
	columns = ["Date:Datetime:110","Doc ID::100","Customer:Link/Customer:200","Status:Link/Visit Status:200","Market Information:Data:200","Sales Rep:Link/Sales Person:200","Route:Link/Territory:200"]
	conditions = ""
	if filters.get("from_date"):
		conditions += " AND dra.dra_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND dra.dra_date <= %(to_date)s"
	if filters.get("sales_rep"):
		conditions += " AND dra.dra_sales_rep = %(sales_rep)s"
	if filters.get("route"):
		conditions += " AND dra.dra_route = %(route)s"
	data = frappe.db.sql("""SELECT dra.dra_date,dra.name,drav.drav_customer,drav.visit_status,drav.market_information,dra.dra_sales_rep,dra.dra_route 
		FROM `tabDaily Route Activity` dra, `tabDaily Route Activity Visit` drav WHERE dra.name = drav.parent %s""" % conditions,filters)
	return columns, data
