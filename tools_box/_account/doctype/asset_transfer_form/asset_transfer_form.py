# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.model.document import Document
from datetime import  datetime

class AssetTransferForm(Document):
	def validate(self):
		if self.status == "Returned":
			self.returned_date = datetime.now()

		if self.workflow_state == "Approved" and not self.approved_by:
			frappe.throw("Please indicate the approver.")



