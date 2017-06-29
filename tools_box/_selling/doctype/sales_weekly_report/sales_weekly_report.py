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
    data = frappe.db.sql(sql, as_dict=1)
    return  data


@frappe.whitelist()
def get_weeks_visits(period_from=None, period_to=None, sales_person=None):
    data = {}
    # Exising
    sql = "select r.dra_date as visited, v.drav_customer customer,v.outlet_type outlet_type ,"\
          "CONCAT( v.market_information, '\n' , v.visit_status ) comment from " \
          "`tabDaily Route Activity` r ,`tabDaily Route Activity Visit` v " \
          "where (r.name = v.parent) and r.dra_sales_rep = '{2}' and DATE(r.dra_date) BETWEEN DATE('{0}') " \
          "and DATE('{1}')".format(period_from,period_to,sales_person)
    data["existing"] = frappe.db.sql(sql, as_dict=1)
    # New
    sql = "select v.* from `tabDaily Route Activity` r ,`tabOutlet Details` v " \
          "where (r.name = v.parent) and r.dra_sales_rep = '{2}' and DATE(r.dra_date) BETWEEN DATE('{0}')"\
          "and DATE('{1}')".format(period_from,period_to,sales_person)
    data["new"] = frappe.db.sql(sql, as_dict=1)
    return data
