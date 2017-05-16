# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Date:Date:200","Purchase Receipt:Link/Purchase Receipt:200","Supplier:Link/Supplier:200",
	"Item Code:Link/Item:200","Item Name:Data:200",
	"Qty Received:Float:75","Qty Accepted:Float:75","Qty Rejected:Float:75","Amount:Currency:200"], []
	item=""
	supplier=""
	if filters.get("item"):
		item = """ and poi.item_code = '{}' """.format(filters.get("item"))
	if filters.get("supplier"):
		supplier = """ and po.supplier = '{}' """.format(filters.get("supplier"))
	data = frappe.db.sql("""select po.posting_date,po.name,po.supplier,poi.item_code,poi.item_name,poi.received_qty,poi.qty,poi.rejected_qty,poi.amount from `tabPurchase Receipt Item` poi 
		join `tabPurchase Receipt` po on poi.parent=po.name 
		where po.docstatus=1 and po.status="Completed" and (po.posting_date between '{}' and '{}') {} {} 
		""".format(filters.get("from"),filters.get("to"),item,supplier),as_list=1 )
	return columns, data
