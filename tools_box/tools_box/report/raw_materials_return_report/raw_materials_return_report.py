# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Date:Date:200","Shift:Data:100","Item Code:Link/Item:200","Item:Data:200","UOM:Link/UOM:75","Qty:Float:100"], []
	#Date	Shift	Item	UOM	Qty
	item=""
	item_group=""
	shift=""
	if filters.get("item"):
		item = """ and i.item_code = "{}" """.format(filters.get("item"))
	if filters.get("item_group"):
		item_group = """ and ii.item_group = "{}" """.format(filters.get("item_group"))
	if filters.get("shift") != "All":
		shift = """ and f.shift="{}" """.format(filters.get("shift"))
	data = frappe.db.sql("""select f.date,f.shift,i.item_code,i.item_name,i.uom,i.qty
		from `tabRaw Materials Return Item` i join `tabRaw Materials Return Form` f on i.parent=f.name 
		join `tabItem` ii on ii.name = i.item_code
		where f.docstatus =1 and (f.date between "{}" and "{}") {} {} {}
		""".format(filters.get("from"),filters.get("to"),item,item_group,shift),as_list=1)
	return columns, data
