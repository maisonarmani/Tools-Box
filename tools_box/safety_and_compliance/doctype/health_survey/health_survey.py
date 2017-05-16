# -*- coding: utf-8 -*-
# Copyright (c) 2015, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
#import  inspect

class HealthSurvey(Document):
	def on_update(self):
		frappe.async.publish_realtime('health_survey_amended',self.as_dict(),doctype=self.doctype,docname=self.name,after_commit=False)
		#frappe.errprint(self.__dict__)


	def before_update(self):
		pass



