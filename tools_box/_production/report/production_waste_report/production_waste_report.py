# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    data, conditions = [], ""
    columns = [
                  "Start Date:Date:200",
                  "Production Order:Link/Production Order:120",
                  "Item:Link/Item:100",
                  "Item Name:Data:100",
                  "UOM:Link/UOM:75",
                  "Produced Qty:Float:100",
                  "Destination Warehouse:Link/Warehouse:100",
                  "Waste:Data:100",
              ]

    if filters.get('production_order'):
        conditions = " and  p.production_order='{production_order}'"

    if filters.get('to') and filters.get("from"):
        conditions += " and (p.planned_start_date between DATE('{from}') and DATE('{to}'))"

    data = frappe.db.sql(
        "SELECT p.planned_start_date,p.production_order,  c.item_code, c.item_name, c.item_uom, c.actual "
        "p,destination_warehouse , c.waste FROM `tabProduction Waste` p JOIN "
        "`tabProduction Waste Manufactured Items` c ON (c.parent = p.name) "
        "WHERE (1=1) {cond}".format(cond=conditions.format(**filters)), as_list=1)

    return columns, data
