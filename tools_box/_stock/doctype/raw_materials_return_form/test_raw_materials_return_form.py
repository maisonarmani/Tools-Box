# -*- coding: utf-8 -*-
# Copyright (c) 2015, bobzz.zone@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest

# test_records = frappe.get_test_records('Raw Materials Return Form')

class TestRawMaterialsReturnForm(unittest.TestCase):
	pass

def tear_down():

	raw_mat_ret_item =  frappe.get_list(doctype="Raw Materials Return Item", filters={
		"parent":"RMRF-00951"
	}, fields=["item_code","item_name","qty", "uom"], order_by="item_code")


	# using the raw material return information use the materials request form to get the mat req to run the reversal on
	nmrf = frappe.new_doc("Stock Entry")
	nmrf.purpose = "Material Receipt"
	nmrf.title = "Material Receipt"
	nmrf.from_warehouse = ""
	nmrf.docstatus = 1

	new_items = []
	for index,value in enumerate(raw_mat_ret_item):

		# Get items default warehouse
		cur_item =  frappe.get_list(doctype="Item", filters={"name":value.item_code}, fields=['default_warehouse'])
		if index == 0:
			nmrf.to_warehouse = cur_item[0].default_warehouse

		# using the latest cost center for item
		last_cost_center = frappe.get_list(doctype="Stock Entry Detail",
								   filters={"item_code": value.item_code}, fields=['cost_center'], order_by='creation')

		d_cost_center = ""
		if last_cost_center[0].get('cost_center') != None:
			d_cost_center = last_cost_center[0].cost_center

		# set new item
		item = dict(
			to_warehouse=cur_item[0].default_warehouse,
			qty=value.qty,
			item_code=value.item_code,
			item_name=value.item_name,
			uom=value.uom,
			cost_center=d_cost_center
		)
		nmrf.append('items',item)
	nmrf.insert()
	nmrf.submit()