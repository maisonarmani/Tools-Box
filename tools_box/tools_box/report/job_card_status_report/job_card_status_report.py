# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Date:Date:200","Doc id:Link/Job Card:200","Ticket No:Data:200","Job Description:Data:200","Vendor:Link/Supplier:200","Job Status:Data:200","Total Job Cost:Currency:200"], []
	#Date	Doc id	Ticket #	Job Descrip	Vendor	Job Status	Total Job cost
	vendor=""
	status=""
	if filters.get("status"):
		status = """ and status = "{}" """.format(filters.get("status"))
	if filters.get("vendor"):
		status = """ and vendor = "{}" """.format(filters.get("vendor"))
	data = frappe.db.sql("""select job_card_date,name,ticket_number,job_description,vendor,status,job_card_total
		from `tabJob Card` where (job_card_date between "{}" and "{}") {} {}
	 """.format(filters.get("from"),filters.get("to"),vendor,status),as_list=1)
	return columns, data
