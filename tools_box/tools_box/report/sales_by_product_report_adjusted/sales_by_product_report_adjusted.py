# Copyright (c) 2017, masonrmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if not filters: filters ={}
	columns = [
		"Item:Link/Item:300",
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
	if filters.get("brand"):
		#conditions += " AND c.brand = %(brand)s"
		pass


	data = frappe.db.sql("""SELECT CONCAT(sii.item_name,' (',sii.item_code,')'),si.posting_date,si.name,si.customer,
		sii.qty,sii.net_amount,sii.amount,c.territory FROM `tabSales Invoice` si, `tabSales Invoice Item` sii, `tabCustomer` c 
		WHERE si.name = sii.parent AND si.docstatus = 1 AND c.name = si.customer %s ORDER BY sii.item_name,si.posting_date""" % conditions,
						 filters)
	return columns, data
