# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
#Date	Customer 	Call Type	Purpose of Call ( We would add as applicable) 	Customers Comment	Sales Admin Remark/ Resolution

def execute(filters=None):
	columns, data = ["Date:Datetime:200","Customer:Link/Customer:200","Call Type:Data:100","Purpose of Call:Data:150","Customer Comment:Data:300","Sales Admin Remark:Data:400","Caller::200"], []
	customer=""
	call_type=""
	call_purpose=""
	if filters.get("customer"):
		customer = """ and customer = "{}" """.format(filters.get("customer"))
	if filters.get("call_type"):
		call_type = """ and call_type = "{}" """.format(filters.get("call_type"))
	if filters.get("call_purpose"):
		call_purpose = """ and call_purpose = "{}" """.format(filters.get("call_purpose"))
	data = frappe.db.sql("""select date,customer,call_type,call_purpose,customer_comment,sales_admin_remark,caller
	from `tabCall Log` where docstatus=1 and (date between "{}" and "{}") {} {} {} 
	""".format(filters.get("from"),filters.get("to"),customer,call_purpose,call_type),as_list=1)
	return columns, data
