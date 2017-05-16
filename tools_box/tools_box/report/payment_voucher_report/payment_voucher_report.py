# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
#Date 	Doc-id	Supplier Name	Ref doc	Amount	Mode of Payment	Bank Name	Ref No
def execute(filters=None):
	columns, data = ["Date:Date:100","Payment Voucher Form:Link/Payment Voucher Form:120",
	"Supplier:Link/Supplier:150","Payment For:Data:200","Ref Doc::130","Amount:Currency:120",
					 "Mode of Payment:Link/Mode Of Payment:150","Bank Name::150","Ref No::150"], []
	supplier,mop,bank="","",""
	if filters.get("supplier"):
		supplier=""" and supplier = "{}" """.format(filters.get("supplier"))
	if filters.get("mop"):
		mop=""" and mode_of_payment = "{}" """.format(filters.get("mop"))
	if filters.get("bank"):
		bank=""" and bank_name = "{}" """.format(filters.get("bank"))
	
	data=frappe.db.sql("""select date,name,supplier , payment_for,ref_doc,amount,mode_of_payment,bank_name,ref_no
	from `tabPayment Voucher Form` where docstatus=1 and (date between '{}' and '{}') {} {} {} 
	""".format(filters.get("from"),filters.get("to"),supplier,mop,bank),as_list=1)
	return columns, data
