# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Date:Date:200","Party:Data:200","Payment Type:Data:200","Amount:Currency:200","Reference Voucher:Link/Payment Entry:200"], []
	payment_type=""
	if filters.get("payment_type") and filters.get("payment_type")!="All":
		payment_type = """ and payment_type = "{}"  """.format(filters.get("payment_type"))
	data = frappe.db.sql("""select posting_date,party,payment_type,IF(party_type="Customer",received_amount,paid_amount),name 
		from `tabPayment Entry` where docstatus=1 and (posting_date between "{}" and "{}") {} """.format(filters.get("from"),filters.get("to"),payment_type),as_list=1)
	return columns, data
