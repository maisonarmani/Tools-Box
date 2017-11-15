# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class SalesJourneyPlan(Document):
    def autoname(self):
        self.name = "%s - %s to %s" % (self.sales_rep, self.get('from'), self.get('to'))


@frappe.whitelist()
def get_current_route(sales_rep, date):
    return {
        'outlets': _get_outlets(sales_rep, date),
        'dra_visits': _get_dra_visits(sales_rep, date)
    }


def _get_outlets(sales_rep, date):
    return frappe.db.sql(
        "SELECT c.customer as outlet_name from `tabSales Journey Plan` p INNER  JOIN `tabSales Journey Plan New Item` c "
        "ON (p.name =c.parent) where p.sales_rep = '%s' and c.date=DATE('%s') " % (sales_rep, date), as_dict=1)


def _get_dra_visits(sales_rep, date):
   return frappe.db.sql(
        "SELECT c.customer as drav_customer from `tabSales Journey Plan` p INNER JOIN `tabSales Journey Plan Existing Item` c "
        "ON (p.name =c.parent) where p.sales_rep = '%s' and c.date=DATE('%s') " % (sales_rep, date), as_dict=1)
