# -*- coding: utf-8 -*-
# Copyright (c) 2015, masonarmani38@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
from frappe.desk.form.load import  get_meta_bundle,get_user_permissions,get_list_settings
# test_records = frappe.get_test_records('Fire Extinguisher')
from frappe.desk.reportview import get_match_cond
class TestFireExtinguisher(unittest.TestCase):
	def nope(self):
		doctype = 'Employee'
		txt = "Sy"
		searchfield = "employee_name"
		start,page_len = 0,10
		filters = { }
		cond = ""

		if filters.get('status'):
			cond = "status= {status}".format(**filters)

		sql = """select name,employee_name from `tabEmployee` where (1=1) and ({key} like %(txt)s) {mcond} order by if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999), name limit %(start)s, %(page_len)s"""\
		    .format(**{
				'key': searchfield,
				'mcond': get_match_cond(doctype)
			}),{
		 'txt': "%%%s%%" % txt,
		 '_txt': txt.replace("%", ""),
		 'start': start,
		 'page_len': page_len
		}
		print(frappe.db.sql(*sql))

	def test_rmP(self):
		doctype = "Vehicle Inspection Checklist",
		with_parent=False,
		cached_timestamp=None
		"""load doctype"""

		docs = []
		parent_dt = None

		# with parent (called from report builder)
		if with_parent:
			parent_dt = frappe.model.meta.get_parent_dt(doctype)
			if parent_dt:
				docs = get_meta_bundle(parent_dt)
				frappe.response['parent_dt'] = parent_dt

		if not docs:
			docs = get_meta_bundle(doctype)

		frappe.response['user_permissions'] = get_user_permissions(docs)
		frappe.response['list_settings'] = get_list_settings(parent_dt or doctype)

		if cached_timestamp and docs[0].modified == cached_timestamp:
			return "use_cache"

		frappe.response.docs.extend(docs)