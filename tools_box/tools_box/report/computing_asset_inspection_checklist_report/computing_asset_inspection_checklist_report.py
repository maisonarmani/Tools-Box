# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
#Employee	Computing Asst Type	Status	Remarks	##Employee Sign
def execute(filters=None):
	columns, data = ["Employee::200","Computing Asset Type::200","Status::150","Remark::200"], []
	status=""
	if filters.get("status"):
		status=""" and d.status = "{}" """.format(filters.get("status"))
	data = frappe.db.sql("""select e.employee_name,d.computing_asset_type,d.status,d.remark 
		from `tabComputing Asset Inspection Item` d 
		join `tabComputing Asset Inspection Checklist` p on d.parent=p.name 
		join `tabEmployee` e on d.employee = e.name
		where p.docstatus=1 and (p.date between "{}" and "{}") {} """.format(filters.get("from"),filters.get("to"),status),as_list=1)
	return columns, data
