# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SalesWeeklyReportConfig(Document):
	def validate(self):
		name_check = ""
		if self.get('__islocal') == None:
			name_check = self.name
		for i, target in enumerate(self.target):
			sql = "select twrc.name from `tabSales Weekly Report Config` twrc,"\
			"`tabSales Team Target` ttt where (ttt.parent = twrc.name) and twrc.name != '{3}' and ttt.sales_executive='{2}' "\
			"and twrc.period_to <= DATE('{0}')  and twrc.period_from >= DATE('{1}') and twrc.enabled = 1 "\
				.format(self.period_to,self.period_from,target.sales_executive,name_check)

			active_target = frappe.db.sql(sql, as_list=1 )
			if len(active_target) > 0:
				frappe.throw("Sorry, {0} already has a target in {1}".format(target.fullname, active_target[0][0] ))

