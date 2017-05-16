# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Bank Name Account::200","Amount:Currency:200"], []
	data = frappe.db.sql("""select gl.account,sum(gl.debit-gl.credit) from `tabGL Entry` gl join `tabAccount` a on gl.account = a.name
	where a.account_type = "Bank" and a.is_group=0  group by gl.account""")
	return columns, data
