import frappe
from frappe.email.doctype.email_queue.email_queue import retry_sending

def resend():
	data = []
	data = frappe.db.sql('select name from `tabEmail Queue` where status = "error" and creation >= DATE("2017-05-30") limit 40', as_list=1)
	for datum in data:
		retry_sending(datum[0])
	print data


def set_employee():
	employee = frappe.get_doc("Employee" ,"GCL-EMP/0882")
	employee.user_id ="Administrator"
	employee.save(ignore_permissions =True)