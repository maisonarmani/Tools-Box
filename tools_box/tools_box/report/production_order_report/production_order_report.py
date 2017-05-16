# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Date:Date:200","WPOF No:Link/Weekly Production Plan:200","Item Code:Link/Item:200","Item Name:Data:200","UOM:Link/UOM:50","Qty:Float:75"], []
	item=""
	item_group=""
	if filters.get("item"):
		item = """ and i.item_code = "{}" """.format(filters.get("item"))
	if filters.get("item_group"):
		item_group = """ and ii.item_group = "{}" """.format(filters.get("item_group"))
	data = frappe.db.sql ("""select f.date,f.name,i.item_code,i.item_name,i.uom,i.qty 
		from `tabWeekly Production Plan Item` i join `tabWeekly Production Plan` f on i.parent=f.name 
		join `tabItem` ii on ii.name = i.item_code
		where f.docstatus =1 and (f.date between "{}" and "{}") {} {}
		""".format(filters.get("from"),filters.get("to"),item,item_group),as_list=1)
	return columns, data
