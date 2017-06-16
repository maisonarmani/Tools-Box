# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class SalesWeeklyReport(Document):
    def validate(self):
        pass


@frappe.whitelist()
def get_sales_target(period_from=None, period_to=None, employee=None):
    sql = "select target.target from `tabSales Weekly Report Config` config, `tabSales Team Target` target where" \
      "(target.parent = config.name) AND target.sales_executive ='{0}' AND (config.period_from <= DATE ('{1}') AND " \
          "config.period_to >=  DATE ('{2}')) AND enabled=1".format(employee, period_from, period_to)
    #frappe.errprint(sql)
    data = frappe.db.sql(sql, as_dict=1)
    return  data
