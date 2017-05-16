# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	#Fixed asst class	Fixed asset name	Status	Remarks
	columns, data = ["Fixed Asset Class::200","Fixed Asset:Link/Asset:200","Status::150","Remarks::200"], []
	asset,category,status="","",""
	if filters.get("status"):
		status=""" and d.status = "{}" """.format(filters.get("status"))
	if filters.get("category"):
		status=""" and p.fixed_asset_class = "{}" """.format(filters.get("category"))
	if filters.get("asset"):
		status=""" and d.fixed_asset = "{}" """.format(filters.get("asset"))
	data = frappe.db.sql("""select p.fixed_asset_class,d.fixed_asset,d.status,d.remark
		from `tabFixed Asset Inspection Item` d 
		join `tabFixed Asset Inspection Checklist` p on d.parent = p.name
		where p.docstatus=1 and (p.date between "{}" and "{}") {} {} {}
		""".format(filters.get("from"),filters.get("to"),status,category,asset),as_list=1)
	return columns, data
