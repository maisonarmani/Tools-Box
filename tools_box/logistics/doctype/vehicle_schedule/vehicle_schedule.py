# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class VehicleSchedule(Document):
	def validate(self):
		for item in self.vehicle_schedule_outbound_item:
			i = frappe.get_list("Vehicle Schedule Outbound Item", {"ref_name":item.ref_name, "docstatus":1})
			if len(i) > 0:
				frappe.throw("Reference name {ref} is already covered ".format(
					ref=item.ref_name))

		for item in self.vehicle_schedule_inbound_item:
			i = frappe.get_list("Vehicle Schedule Inbound Item", {"ref_name": item.ref_name, "docstatus": 1})
			if len(i) > 0:
				frappe.throw("Reference name {ref} is already covered ".format(
					ref=item.ref_name))


@frappe.whitelist(True)
def get_daily_cost(vehicle = None):
	if vehicle:
		daily_cost = frappe.get_list("Vehicle Daily Cost", filters={
			"vehicle": vehicle,
			"enabled":1
		}, fields= ['total_cost'])

		if not len(daily_cost):
			return 0
		else:
			return daily_cost[0].get('total_cost')
	return 0

@frappe.whitelist(True)
def get_total(doctype = None, docname = None):
	if doctype and docname:
		total = frappe.get_list(doctype, filters={
			"name": docname,
			"docstatus":1
		}, fields= ['total'])

		if not len(total):
			return 0
		else:
			return total[0].get('total')
	return 0

@frappe.whitelist(True)
def get_allowed():
	ls = frappe.get_single("Logistics Settings")
	if ls:
		return dict(
			outbound=ls.get("allowed_outbound_cost"),
			inbound=ls.get("allowed_inbound_cost")
		)


