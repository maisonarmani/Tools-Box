# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	#S/N	Date	Doc id	Request Type	Subject	Raised By	Status	Assigned to
	columns, data = ["Date:Datetime:200","Doc id:Link/Helpdesk Ticket:200","Request Type:Link/Request Type:150","Subject:Data:200","Raised By::150","Status:Data:150","Assigned to:Link/Employee:200"], []
	request=""
	status=""
	raised=""
	if filters.get("request"):
		request = """ and request_type = '{}' """.format(filters.get("request"))
	if filters.get("status"):
		status = """ and status = '{}' """.format(filters.get("status"))
	if filters.get("raised"):
		raised = """ and raised_by = '{}' """.format(filters.get("raised"))
	data=frappe.db.sql("""select addtime(opening_date,opening_time) as "date",name,request_type,subject,raised_by_name,status,assigned_to_name
	from `tabHelpdesk Ticket`
	where (opening_date between "{}" and "{}") {} {} {} """.format(filters.get("from"),filters.get("to"),request,status,raised),as_list=1)
	return columns, data
