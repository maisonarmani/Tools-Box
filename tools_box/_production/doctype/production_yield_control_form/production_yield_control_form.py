# -*- coding: utf-8 -*-
# Copyright (c) 2015, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ProductionYieldControlForm(Document):
	pass


@frappe.whitelist(False)
def get_yield(production_order=None):
	if production_order != None:
		prod = frappe.get_list(doctype="Production Order", filters={
			"name": production_order,
		}, fields=['production_item as item_code','qty as expected_output'])

		for itm in prod:
			item = frappe.get_list(doctype="Item", filters={
				"name": itm.item_code,
			}, fields=['item_name', 'stock_uom as uom'])

			# check the finished goods transfer form for excesses
			fgtf = frappe.db.sql("""select c.qty as excess from  `tabFinished Goods Transfer Form` p  JOIN  `tabFinished Goods Transfer Item` c
						ON p.name = c.name  WHERE p.weekly_production_order_form = '%s'""" % production_order, as_list=1)
			excess = 0
			if len(fgtf) > 0 and fgtf[0].get('excess') != None:
				excess = fgtf[0].get('excess')
			itm.update(item[0])
			itm.update({
				"actual_output": itm.expected_output + excess
			})

		return prod
	return []
