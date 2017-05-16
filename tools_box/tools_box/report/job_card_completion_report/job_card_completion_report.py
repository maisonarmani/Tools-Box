# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Date:Date:200","Doc id:Link/Job Card:200","Vendor:Link/Supplier:200","Completion Date:Date:200","Verified By:Data:200"], []
	#Date	doc id	Vendor	Completion date	Job verified by
	vendor=""
	if filters.get("vendor"):
		status = """ and jc.vendor = "{}" """.format(filters.get("vendor"))
	data = frappe.db.sql("""select jc.job_card_date,jc.name,vendor,jc.job_completion_date,e.employee_name
		from `tabJob Card` jc
		join `tabEmployee` e on jc.job_completion_verified_by=e.name
		where (jc.job_card_date between "{}" and "{}") {}
	 """.format(filters.get("from"),filters.get("to"),vendor),as_list=1)

	return columns, data
