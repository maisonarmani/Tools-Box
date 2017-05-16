# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Date:Date:200","Purchase Invoice:Link/Purchase Invoice:200","Supplier:Link/Supplier:200","Qty:Float:100","UOM:Data:100","Amount:Currency:200"], []
	supplier=""
	if filters.get("supplier"):
		supplier=""" and p.supplier ="{}" """.format(filters.get("supplier"))
	data = frappe.db.sql("""select p.posting_date,p.name,p.supplier,d.qty,d.uom,d.amount
	from `tabPurchase Invoice Item` d 
	join `tabPurchase Invoice` p on d.parent=p.name
	where p.docstatus=1
	and (p.posting_date between "{}" and "{}")
	and  d.item_code = "{}"
	{} """.format(filters.get("from"),filters.get("to"),filters.get("item"),supplier),as_list=1)
	return columns, data
