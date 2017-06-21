# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class StaffReplacementRequestForm(Document):
	def validate(self):
		status = str(self.status)
		if status is not "Open":
			if [self.modified_by] not in self.get_approvers():
				frappe.throw("Only specified approver can approve or reject this document")
			self.docstatus = 1

		if str(self.supervisor) is str(self.staff_to_be_replaced):
			frappe.throw("Sorry, Supervisor can not replace him/herself.")

	def get_approvers(self):
		return frappe.db.sql("""
				select u.name from tabUser u, `tabHas Role` r where (u.name = r.parent) and r.role = 'Directors' and 
				u.enabled = 1""", as_list=1)
