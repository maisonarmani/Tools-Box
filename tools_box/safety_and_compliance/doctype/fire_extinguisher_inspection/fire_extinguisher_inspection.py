# -*- coding: utf-8 -*-
# Copyright (c) 2015, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class FireExtinguisherInspection(Document):
	def validate(self):
		""" Document Validation Code Should Affixed Here"""
		fire_extinguishers = []
		could_not_save = "<b>{0} could not be saved.</b><br>".format(self.name)

		for fire_extinguisher in self.fire_extinguisher:
			print(dir(fire_extinguisher))
			if fire_extinguisher.fire_extinguisher in fire_extinguishers:
				frappe.throw(_("{0}Inspected Fire Extinguisher Must be Unique".format(could_not_save)))
			fire_extinguishers.append(fire_extinguisher.fire_extinguisher)

	def on_update(self):
    	# we also need to update the fire extinguisher table with the new status
		for inspected_fire_extinguisher in self.fire_extinguisher:
			try:
				frappe.set_value ("Fire Extinguisher",inspected_fire_extinguisher.fire_extinguisher,'status',inspected_fire_extinguisher.status)
			except Exception as exception:
				pass

	def before_trash(self):
		pass	
