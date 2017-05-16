# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	#Date | Supplier | Item Description | Status Report | Updated By
	columns, data = ["Date:Date:200","Purchase Order:Link/Purchase Order:125","Supplier:Link/Supplier:150","Status:Data:300","Updated By:Data:150"], []
	supplier=""
	purchase_order=""
	if filters.get("supplier"):
		supplier=""" and p.supplier = "{}" """.format(filters.get("supplier"))
	if filters.get("purchase_order"):
		purchase_order=""" and p.name = "{}" """.format(filters.get("purchase_order"))
	data = frappe.db.sql("""select s.modified,s.purchase_order,p.supplier,s.status,s.modified_by
	from `tabPurchase Order Status` s 
	join `tabPurchase Order` p on p.name = s.purchase_order
	where s.docstatus=1 and p.docstatus=1 and (CAST(s.modified AS DATE) between "{}" and "{}") {} {} """.format(filters.get("from"),filters.get("to"),supplier,purchase_order),as_list=1)
	return columns, data
