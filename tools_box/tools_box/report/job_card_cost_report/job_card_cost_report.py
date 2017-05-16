# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	#Date	Doc id 	Vendor	Materials Total	Labour Fees	Transport	Total	Advance	Status
	columns, data = ["Date:Date:200","Doc id:Link/Job Card:200","Vendor:Link/Supplier:200","Materials Total:Currency:200",
	"Labour Fees:Currency:200","Transport Fare:Currency:200","Total:Currency:200","Job Advance:Currency:200","Job Status:Data:200"], []
	vendor=""
	if filters.get("vendor"):
		status = """ and vendor = "{}" """.format(filters.get("vendor"))
	data = frappe.db.sql("""select job_card_date,name,vendor,materials_total,labour_fees,transport_fare,job_card_total,job_advance,status
		from `tabJob Card` where (job_card_date between "{}" and "{}") {}
	 """.format(filters.get("from"),filters.get("to"),vendor),as_list=1)
	return columns, data
