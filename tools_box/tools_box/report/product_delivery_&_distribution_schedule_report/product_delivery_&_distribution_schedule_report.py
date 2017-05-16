# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Delivery Date:Date:200","Customer:Link/Customer:200","Item Code:Link/Item:200","Item Name:Data:200","Qty:Float:200","Territory:Link/Territory:200","Sales:Data:200"], []
	item=""
	customer=""
	territory=""
	item_group=""
	if filters.get("item"):
		item = """ and soi.item_code = '{}' """.format(filters.get("item"))
	if filters.get("customer"):
		customer = """ and so.customer = '{}' """.format(filters.get("customer"))
	if filters.get("territory"):
		territory = """ and so.territory = '{}' """.format(filters.get("territory"))
	if filters.get("item_group"):
		item_group = """ and soi.item_group = '{}' """.format(filters.get("item_group"))
	data = frappe.db.sql("""select so.delivery_date,so.customer,soi.item_code,soi.item_name,soi.qty,so.territory,so.sales_partner
	from `tabSales Order Item` soi join `tabSales Order` so on soi.parent=so.name 
	where so.delivery_date = '{}' {} {} {} {} group by soi.name,so.delivery_date,so.customer order by soi.item_name""".format(filters.get("delivery"),item,territory,customer,item_group),as_list=1)
	return columns, data
