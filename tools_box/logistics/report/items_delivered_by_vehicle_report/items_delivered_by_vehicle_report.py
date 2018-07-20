# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    columns, data = ["Vehicle Schedule:Link/Vehicle Schedule:130", "Vehicle:Link/Vehicle:130",
                     "Item Code:Link/Item:130", "Item Name:Data:260", "Qty:Float:100"], []

    conds = ""
    if filters.get('from_date') and filters.get('to_date'):
        conds += " AND d.posting_date BETWEEN DATE('%s') AND DATE('%s')" % (
        filters.get('from_date'), filters.get('to_date'))

    if filters.get('vehicle'):
        conds += " AND p.vehicle = '%s'" % filters.get('vehicle')

    data = frappe.db.sql(
        "SELECT p.name ,p.vehicle,dc.item_code, dc.item_name , SUM(dc.qty) FROM `tabVehicle Schedule` p INNER JOIN "
        "`tabVehicle Schedule Outbound Item` c ON(p.name = c.parent) INNER  JOIN `tabDelivery Note` d INNER JOIN "
        "`tabDelivery Note Item` dc  ON(d.name = dc.parent) WHERE d.name = c.ref_name %s GROUP BY dc.item_name, p.vehicle" % conds)


    return columns, data
