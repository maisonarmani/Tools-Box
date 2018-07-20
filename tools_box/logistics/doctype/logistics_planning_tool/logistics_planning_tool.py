# -*- coding: utf-8 -*-
# Copyright (c) 2018, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class LogisticsPlanningTool(Document):
    def autoname(self):
        if self.customer:
            self.name = "{0}-{1}-{2}".format(self.customer, self.territory, self.schedule_delivery_date)
        else:
            self.name = "{0}-{1}".format(self.territory, self.schedule_delivery_date)


@frappe.whitelist(True)
def get_atls(ps, pe, territory=None, customer=None, include_pending=None):
    conds = ""

    if territory and str(territory) != str("Nigeria"):
        conds += ' AND territory = "%s" ' % territory
    if customer:
        conds += ' AND customer = "%s" ' % customer

    if not include_pending:
        conds += " AND delivery_date BETWEEN DATE('%s') AND DATE('%s') " % (ps, pe)

    return frappe.db.sql(
        "SELECT name as authority_to_load, IFNULL(delivery_date, transaction_date) as delivery_date , customer, territory from `tabAuthority to Load` WHERE name NOT IN (SELECT l.name FROM `tabLogistics Planning Tool` l INNER JOIN `tabLogistics Planning Tool Detail` c ON(l.name=c.parent) WHERE c.status != 'Delivered') %s ORDER BY territory " % (
        conds), as_dict=1)
