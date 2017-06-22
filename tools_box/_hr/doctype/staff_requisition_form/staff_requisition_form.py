# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class StaffRequisitionForm(Document):
    def validate(self):
        st = str(self.status)
        if st in ["Approved", "Rejected"]:
            if [self.modified_by] not in self.get_approvers():
                frappe.throw("Only specified approver can approve or reject this document")
            self.docstatus = 1

    def get_approvers(self):
        return frappe.db.sql("""
				select u.name from tabUser u, `tabHas Role` r where (u.name = r.parent) and r.role = 'Directors' and 
				u.enabled = 1""", as_list=1)


@frappe.whitelist()
def get_approvers(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
		select u.name, concat(u.first_name, ' ', u.last_name)
		from tabUser u, `tabHas Role` r
		where u.name = r.parent and r.role = 'Directors' 
		and u.enabled = 1 and u.name like %s
	""", ("%" + txt + "%"))
