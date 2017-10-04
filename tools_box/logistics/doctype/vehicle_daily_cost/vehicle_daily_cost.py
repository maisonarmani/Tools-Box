# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class VehicleDailyCost(Document):
	def validate(self):
		if self.check_enabled_vehicle():
			frappe.throw("Sorry, Unable to save, Vehicle daily cost can only have one active vehicle")


	def check_enabled_vehicle(self):
		daily_cost = frappe.get_list("Vehicle Daily Cost", filters={
			"vehicle": self.vehicle,
			"enabled": 1
		}, fields=['name'])

		return len(daily_cost) and daily_cost[0].name != self.name