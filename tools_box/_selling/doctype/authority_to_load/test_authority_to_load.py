# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest

# test_records = frappe.get_test_records('Authority to Load')

class TestAuthoritytoLoad(unittest.TestCase):
	def test1(self):
		sales_order = "GCL-SO-09723"
		doc = frappe.get_all('Sales Order', fields=['title'], filters=[["name", "=", sales_order]],
							 ignore_permissions=True)
		print(doc.pop().title)

	def test2(self):
		filters = {}
		conditions = ""
		if filters.get("from_date"):
			conditions += " AND vs.date >= %(from_date)s"
		if filters.get("to_date"):
			conditions += " AND vs.date <= %(to_date)s"
		if filters.get("vehicle"):
			conditions += " AND vs.vehicle = %(vehicle)s"
		if filters.get("driver"):
			conditions += " AND vs.driver = %(driver)s"
		if filters.get("delivery_note"):
			conditions += " AND vsd.delivery_note = %(delivery_note)s"
		data = frappe.db.sql(
			"SELECT vs.date,vs.name,vs.vehicle,vs.driver,vs.sales_rep,vsd.delivery_note,dn.grand_total FROM (`tabVehicle Schedule` vs LEFT JOIN `tabVehicle Schedule Delivery` vsd ON (vs.name = vsd.parent)) LEFT OUTER JOIN  `tabDelivery Note` dn  ON (dn.name = vsd.delivery_note) WHERE vs.docstatus=1 {0} limit 1".format(
				conditions), filters)
		print(data)
