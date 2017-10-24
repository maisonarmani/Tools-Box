# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class OvertimeRequest(Document):
	def on_change(self):
		if self.workflow_state == "Approved":
			c_employee = frappe.get_value("Employee", {"user_id": frappe.session.get('user')}, "name")
			if self.approved_by != c_employee:
				frappe.throw("Sorry, this document can only be approved by %s" %
							 self.approved_by)

		elif self.workflow_state == "Authorized":
			c_employee = frappe.get_value("Employee", {"user_id": frappe.session.get('user')}, "name")
			if self.authorized_by != c_employee:
				frappe.throw("Sorry, this document can only be authorized by and %s" %
							 self.authorized_by)

@frappe.whitelist()
def make_overtime_sheet(docname):
	overtime_req = frappe.get_doc("Overtime Request", docname)

	overtime_sht = frappe.new_doc("Overtime Sheet")
	overtime_sht.overtime_request =  overtime_req.name
	overtime_sht.raised_by = overtime_req.requested_by
	overtime_sht.raised_by_name = overtime_req.requested_by_name
	overtime_sht.department = overtime_req.department
	overtime_sht.date = overtime_req.date
	overtime_sht.start_time = overtime_req.start_time
	overtime_sht.number_of_employees = overtime_req.number_of_employee_required
	overtime_sht.end_time = overtime_req.end_time

	return overtime_sht.as_dict()