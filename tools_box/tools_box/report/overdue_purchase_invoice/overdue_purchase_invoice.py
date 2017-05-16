# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
#Supplier Name	Outstanding Amount	Invoice #	Days Overdue
def execute(filters=None):
	columns, data = ["Supplier Name:Link/Supplier:200","Outstanding Amount:Currency:200","Invoice:Link/Purchase Invoice:200","Days Overdue"], []
	where=""
	if filters.get("supplier"):
		where = """ and i.supplier = "{}" """.format(filters.get("supplier"))
	data = frappe.db.sql("""
		select * from 
		(select i.supplier,i.outstanding_amount,i.name,datediff(i.due_date,NOW()) as 'days' 
		from `tabPurchase Invoice` i where i.docstatus=1 and i.outstanding_amount>0 and (i.posting_date between '{}' and '{}') {} ) d
		where d.days<0 """.format(filters.get("from"),filters.get("to"),where),as_list=1)
	return columns, data
