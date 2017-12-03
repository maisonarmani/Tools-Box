# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest


class TestStationariesRequest(unittest.TestCase):
    pass


def manufactured():
    d = frappe.db.sql(
        "SELECT i.name,i.item_name, i.stock_uom ,SUM(po.produced_qty) from `tabItem` i RIGHT OUTER JOIN `tabProduction Order` po "
        "ON(i.name = po.production_item) WHERE i.is_purchase_item = 0 GROUP BY i.name")
    print d


def issued():
    d = frappe.db.sql("SELECT i.name,i.item_name, i.stock_uom ,SUM(sed.qty) from `tabItem` i INNER JOIN "
                      "`tabStock Entry` se RIGHT OUTER JOIN `tabStock Entry Detail` sed ON((i.name = sed.item_code) and (sed.parent = se.name) ) "
                      "WHERE se.purpose = 'Material Issue' AND i.is_purchase_item = 0 GROUP BY i.name")
    print d
