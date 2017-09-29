# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest

class TestProductionWaste(unittest.TestCase):
	pass


def tear_down():
	filters =dict({
		"from" : "01-09-2017 17:49:55",
		"to":"01-12-2017 17:49:55",
		"production_order":"GCL-PRO-17-00006"
	})
	conditions = ""

	from datetime import datetime
	froms = unicode.split(filters.get("from")," ")
	tos =  unicode.split(filters.get("to")," ")
	filters['to']=datetime.strptime(tos[0], "%d-%m-%Y").strftime("%Y-%m-%d")+" "+ tos[1]
	filters['from']=datetime.strptime(froms[0], "%d-%m-%Y").strftime("%Y-%m-%d")+" "+froms[1]


	if filters.get('production_order'):
		conditions = " and  p.production_order='{production_order}'"

	if filters.get('to') and filters.get("from"):
		conditions += " and (p.planned_start_date between DATE('{from}') and DATE('{to}'))"

	data = frappe.db.sql(
		"SELECT p.production_order, p.planned_start_date, c.item_code, c.item_name, c.item_uom, c.actual "
		"p,destination_warehouse , c.waste FROM `tabProduction Waste` p JOIN "
		"`tabProduction Waste Manufactured Items` c ON (c.parent = p.name) "
		"WHERE (1=1) {cond}".format(cond=conditions.format(**filters)), as_list=1)

	print "SELECT p.production_order, p.planned_start_date, c.item_code, c.item_name, c.item_uom, c.actual "\
		"p,destination_warehouse , c.waste FROM `tabProduction Waste` p JOIN "\
		"`tabProduction Waste Manufactured Items` c ON (c.parent = p.name) "\
		"WHERE (1=1) {cond}".format(cond=conditions.format(**filters))
	print data
	return

	allowable_waste = frappe.get_single("Production Waste Setup")
	frappe.errprint(allowable_waste.allowable_waste)
	production_order = "GCL-PRO-17-00006"

	print get_excess(production_order=production_order)
	print get_production_items(production_order=production_order)
	print get_manufactured_items(production_order=production_order)

def get_production_items(production_order=None):
	if production_order:
		stock_entry_details = frappe.db.sql("""select sd.qty, sd.item_name , sd.item_code , sd.uom from `tabStock Entry` s JOIN
						`tabStock Entry Detail` sd ON s.name = sd.parent  WHERE s.production_order = '%s'
						and s.purpose = "Material Transfer for Manufacture" """ %
											production_order, as_list=1)
		return stock_entry_details
	return []


def get_manufactured_items(production_order=None):
	if production_order:
		stock_entry_details = frappe.db.sql("""select sd.qty, sd.item_name , sd.item_code , sd.uom from `tabStock Entry` s JOIN
				`tabStock Entry Detail` sd ON s.name = sd.parent  WHERE s.production_order = '%s'
				and s.purpose = "Manufacture" and sd.t_warehouse != "" GROUP BY s.production_order"""
									% production_order, as_list=1)
		return stock_entry_details
	return []


def get_excess(production_order = None):
	excess = 0
	if production_order:
		fgtf = frappe.db.sql("""select sum(c.qty) excess from `tabFinished Goods Transfer Form` p  JOIN
                  `tabFinished Goods Transfer Item` c ON p.name = c.parent  WHERE p.weekly_production_order_form = '%s'
                    GROUP BY weekly_production_order_form""" % production_order, as_list=1)
		if len(fgtf):
			excess = fgtf[0][0]

	return excess

