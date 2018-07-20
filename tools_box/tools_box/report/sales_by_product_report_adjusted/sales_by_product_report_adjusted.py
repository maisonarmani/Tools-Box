# Copyright (c) 2017, masonrmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if not filters: filters ={}
	columns = [
		"Item:Link/Item:300",
		"Item Group:Link/Item Group:140",
		"Invoice Date:Date:110",
		"Sales Invoice::100",
		"Customer:Link/Customer:200",
		"Qty:Float:50",
		"Amount With Discount:Currency:100",
		"Amount Without Discount:Currency:100",
		"Territory:Link/Territory:100"
	]

	conditions = ""
	if filters.get("from_date"):
		conditions += " AND si.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND si.posting_date <= %(to_date)s"
	if filters.get("customer"):
		conditions += " AND si.customer = %(customer)s"
	if filters.get("item"):
		conditions += " AND sii.item_code = %(item)s"
	if filters.get("territory"):
		conditions += " AND c.territory = %(territory)s"


	data = frappe.db.sql("""SELECT sii.item_name, i.item_group, si.posting_date,si.name,si.customer,
		sii.qty,sii.net_amount,sii.amount,c.territory FROM `tabSales Invoice` si INNER JOIN `tabSales Invoice Item` sii 
		ON(sii.parent = si.name)  INNER JOIN `tabCustomer` c ON(si.customer=c.name) INNER JOIN `tabItem` i 
		ON(i.name=sii.item_code)WHERE si.docstatus = 1%s ORDER BY sii.item_name,si.posting_date""" % conditions,filters)
	return columns, data
