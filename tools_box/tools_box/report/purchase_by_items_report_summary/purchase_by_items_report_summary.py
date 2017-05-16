# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Item:Link/Item:200","Item Name:Data:200","Qty:Float:200","Amount:Currency:200"], []
	item=""
	supplier=""
	territory=""
	if filters.get("item"):
		item = """ and soi.item_code = '{}' """.format(filters.get("item"))
	if filters.get("supplier"):
		supplier = """ and so.supplier = '{}' """.format(filters.get("supplier"))
	data = frappe.db.sql("""select soi.item_code,soi.item_name,sum(soi.qty),sum(soi.amount) from `tabPurchase Invoice Item` soi 
		join `tabPurchase Invoice` so on soi.parent=so.name where so.docstatus=1 and (so.posting_date between '{}' and '{}') {} {} group by soi.item_code""".format(filters.get("from"),filters.get("to"),item,supplier),as_list=1 )
	return columns, data
