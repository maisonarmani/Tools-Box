# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = [
		"Item Code:Link/Item:100",
		"Item Name:Data:250",
		"UOM:Data:150",
		"Qty:Link/Item:100",]

	conditions = " AND (po.planned_start_date BETWEEN DATE({from_date}) and DATE({to_date})) "

	data = frappe.db.sql(
		"SELECT i.name,i.item_name, i.stock_uom ,SUM(po.produced_qty) from `tabItem` i RIGHT OUTER JOIN `tabProduction Order` po "
		"ON(i.name = po.production_item) WHERE i.is_purchase_item = 0  {0} GROUP BY i.name".format(conditions.format(**filters)))

	return columns, data
