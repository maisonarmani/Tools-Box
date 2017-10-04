# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ProductionWaste(Document):
	pass

@frappe.whitelist(False)
def get_production_details(production_order = None):
	prod_items = _get_production_items(production_order)
	manu_items = _get_manufactured_items(production_order)
	if prod_items is not []:
		for item in prod_items:
			item.returned =  _get_returns(production_order, item.item_code)
			item.used =  _get_used(production_order, item.item_code)
			item.waste = (float(item.returned) + float(item.used)) - float(item.issued)

	if manu_items is not []:
		for item in manu_items:
			item.excess = _get_excess(production_order, item.item_code)
			item.expected = _get_expected(production_order)
			item.waste = _get_waste(item)

	return {
		"production_items":prod_items,
		"manufactured_items":manu_items
	}


def _get_waste(item):
	setup = frappe.get_single("Production Waste Setup")
	if setup:
		diff = float(item.actual) - float(item.expected)
		waste = (setup.allowable_waste / 100) * float(item.expected)
		if waste < diff:
			return diff
		else:
			return 0
	return 0

def _get_production_items(production_order=None):
	if production_order:
		stock_entry_details = frappe.db.sql("""select  sd.item_name, sd.item_code, sd.uom item_uom ,SUM(sd.qty) issued from `tabStock Entry` s JOIN
						`tabStock Entry Detail` sd ON s.name = sd.parent  WHERE s.production_order = '%s'
						and s.purpose = "Material Transfer for Manufacture" and s.docstatus = 1 GROUP BY sd.item_code""" %
											production_order, as_dict=1)
		return stock_entry_details
	return []


def _get_manufactured_items(production_order=None):
	if production_order:
		po = frappe.db.sql("""select p.produced_qty actual, i.item_name , i.item_code , i.stock_uom item_uom from `tabItem` i JOIN
				`tabProduction Order` p ON i.name = p.production_item  WHERE p.name = '%s'""" % production_order, as_dict=1)
		return po
	return []

def _get_expected(production_order = None):
	if production_order:
		expected = frappe.db.sql("""select qty from `tabProduction Order` WHERE (name = '%s')"""
							 % production_order, as_dict=1)
		if len(expected) > 0:
			return expected[0].get('qty') or '0'
	return 0


def _get_used(production_order = None, item=None):
	if production_order and item:
		used = frappe.db.sql("""select SUM(c.qty) qty from `tabStock Entry` p  JOIN
                  `tabStock Entry Detail` c ON p.name = c.parent  WHERE (p.production_order = '%s'
                  and c.item_code= '%s') and p.purpose = 'Manufacture' and s_warehouse != '' and p.docstatus = 1 GROUP BY c.item_code"""
							 % (production_order, item ), as_dict=1)
		frappe.errprint(used)
		if len(used) > 0:
			return used[0].get('qty') or '0'
	return 0



def _get_excess(production_order = None, item=None):
	if production_order and item:
		excess = frappe.db.sql("""select c.qty excess from `tabFinished Goods Transfer Form` p  JOIN
                  `tabFinished Goods Transfer Item` c ON p.name = c.parent  WHERE (p.weekly_production_order_form = '%s'
                  and c.item_code= '%s') and p.workflow_state = 'Received' and p.docstatus = 1""" % (production_order ,item) , as_dict=1)
		if len(excess) > 0:
			return excess[0].get('qty') or '0'
	return 0


def _get_returns(production_order = None, item = None):
	if production_order and item:
		returns = frappe.db.sql("""select c.qty from `tabRaw Materials Return Form` p  JOIN `tabRaw Materials Return Item`
					c ON p.name = c.parent  WHERE (p.production_order = '%s' and c.item_code = '%s') and
					 p.workflow_state = 'Received' and p.docstatus = 1""" %( production_order , item) , as_dict=1)
		if len(returns) > 0:
			return returns[0].get('qty') or '0'
	return 0

