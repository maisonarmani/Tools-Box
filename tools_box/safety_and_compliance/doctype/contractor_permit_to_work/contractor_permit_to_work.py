# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ContractorPermittoWork(Document):
	pass


@frappe.whitelist()
def get_approvers(doctype, txt, searchfield, start, page_len, filters):
	return get_approver_list(filters.get("user"), filters.get('role'))


def get_approver_list(name=None, role= None):
	return frappe.db.sql("""select user.name, user.first_name, user.last_name from
		tabUser user, `tabHas Role` user_role where
		user_role.role = '{role}' and user_role.parent = user.name and user.enabled and
		user.name != '{name}' """.format(role=role,name=name))
