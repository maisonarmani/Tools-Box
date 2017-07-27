# -*- coding: utf-8 -*-
# Copyright (c) 2015, masonarmani38@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest

# test_records = frappe.get_test_records('Vehicle Schedule Log')

class TestVehicleScheduleLog(unittest.TestCase):
	def test_ram(self):
		def new_archive(doctype="File", docname=None):
			directories = ["Certificates", "Employee Documents", "Permits", "Logs"]
			if doctype and docname:
				for directory in directories:
					doc = frappe.get_doc({
						"doctype": "File",
						"name": "Home/{}/{}".format(docname, directory),
						"old_parent": "Home/{}".format(docname),
						"folder": "Home/{}".format(docname),
						"is_home_folder": 0,
						"is_private": 0
					})
					doc.insert()

		new_archive("File","Flower")