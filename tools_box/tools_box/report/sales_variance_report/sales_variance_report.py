# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Item:Link/Item:200","Item Name:Data:200","Total Ordered:Float:200","Total Delivered:Float:200","Variance:Float:200"], []
	so_item=""
	dn_item=""
	so_item_group=""
	dn_item_group=""
	if filters.get("item"):
		dn_item = """ and dni.item_code = '{}' """.format(filters.get("item"))
		so_item = """ and soi.item_code = '{}' """.format(filters.get("item"))
	if filters.get("item_group"):
		so_item_group = """ and soi.item_group = '{}' """.format(filters.get("item_group"))
		dn_item_group = """ and dni.item_group = '{}' """.format(filters.get("item_group"))
	data=frappe.db.sql("""select oo.item_code, oo.item_name,oo.amount,dd.amount,(oo.amount-dd.amount) as total
		from (select soi.item_code, soi.item_name, sum(soi.qty) as amount
		from `tabSales Order Item` soi join `tabSales Order` so on soi.parent=so.name 
		where so.docstatus=1 and (so.transaction_date between '{0}' and '{1}') {2} {3} group by soi.item_code) as oo
		join (select dni.item_code, dni.item_name, sum(dni.qty) as amount
		from `tabDelivery Note Item` dni join `tabDelivery Note` dn on dni.parent=dn.name 
		where dn.docstatus=1 and (dn.posting_date between '{0}' and '{1}') {4} {5} group by dni.item_code) as dd on oo.item_code = dd.item_code
	"""
		.format(filters.get("from"),filters.get("to"),so_item,so_item_group,dn_item,dn_item_group),as_list=1)
	return columns, data
