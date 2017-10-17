# -*- coding: utf-8 -*-
# Copyright (c) 2016, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RawMaterialsReturnForm(Document):
	def on_change(self):
		if self.workflow_state == "Approved":
			nmrf = frappe.new_doc("Stock Entry")
			nmrf.purpose = "Material Receipt"
			nmrf.title = "Material Receipt"
			nmrf.from_warehouse = ""
			nmrf.production_order = self.production_order

			new_items = []
			for index, value in enumerate(self.items):

				# Get items default warehouse
				cur_item = frappe.get_list(doctype="Item", filters={"name": value.item_code},
										   fields=['default_warehouse'])

				if index == 0:
					nmrf.to_warehouse = cur_item[0].default_warehouse

				if nmrf.to_warehouse == "":
					frappe.throw("Item {0} does not have default warehouse required for material receipt" .format(value.item_code))
				# using the latest cost center for item
				last_cost_center = frappe.get_list(doctype="Stock Entry Detail",
												   filters={"item_code": value.item_code}, fields=['cost_center'],
												   order_by='creation')

				d_cost_center = ""
				if last_cost_center[0].get('cost_center') != None:
					d_cost_center = last_cost_center[0].cost_center

				# set new item
				item = dict(
					t_warehouse=cur_item[0].default_warehouse,
					qty=value.qty,
					item_code=value.item_code,
					item_name=value.item_name,
					uom=value.uom,
					cost_center=d_cost_center
				)
				nmrf.append('items', item)

			nmrf.insert()
			nmrf.submit()



@frappe.whitelist(False)
def get_production_items(production_order = None):
	if production_order != None:
		# get the stock entry record for the particular production order
		stock_entry =frappe.get_list(doctype="Stock Entry",filters= {
			"production_order":production_order,
			"purpose":"Material Transfer for Manufacture"
		},fields=['name'])

		if stock_entry[0].get('name') != None:
			stock_entry_details = frappe.get_list(doctype="Stock Entry Detail", filters={
				"parent": stock_entry[0].get('name')
			}, fields=['item_code','item_name','qty','uom'])
			return  stock_entry_details
	return []


