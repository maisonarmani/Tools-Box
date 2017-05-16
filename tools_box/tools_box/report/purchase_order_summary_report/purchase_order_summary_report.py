# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Date:Date:200","Status:Data:75","Purchase Order:Link/Purchase Order:200","Supplier:Link/Supplier:200","Item:Link/Item:200","Item Name:Data:200","Ordered Qty:Float:200","Amount:Currency:200"], []
	item=""
	supplier=""
	owner=""
	if filters.get("item"):
		item = """ and poi.item_code = '{}' """.format(filters.get("item"))
	if filters.get("supplier"):
		supplier = """ and po.supplier = '{}' """.format(filters.get("supplier"))
	if filters.get("created"):
		owner=" and po.owner like '%{}%' ".format(filters.get("created"))
	data = frappe.db.sql("""select po.transaction_date,po.workflow_state,po.name,po.supplier,poi.item_code,poi.item_name,poi.qty,poi.amount from `tabPurchase Order Item` poi 
		join `tabPurchase Order` po on poi.parent=po.name 
		where  po.workflow_state="Approved" and (po.transaction_date between '{}' and '{}') {} {} {} 
		""".format(filters.get("from"),filters.get("to"),item,supplier,owner),as_list=1 )
	return columns, data
