# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ContractorWorkPermit(Document):
	pass


@frappe.whitelist()
def get_approvers(doctype, txt, searchfield, start, page_len, filters):
	return get_approver_list(filters.get("user"), filters.get('roles'))


def get_approver_list(name=None, roles= None):
	return frappe.db.sql("""select DISTINCT user.name, user.first_name, user.last_name from
		tabUser user, `tabHas Role` user_role where
		user_role.role in {roles} and user_role.parent = user.name and user.enabled and
		user.name != '{name}' """.format(roles=roles,name=name))
