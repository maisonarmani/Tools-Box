# Copyright (c) 2013,masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    columns, data = ["Name:Link/Finished Goods Transfer Form:140","Date:Date:120", "Production Order:Link/Production Order:150", "Item Code:Link/Item:100",
                     "Item Name:Data:200", "UOM:Link/UOM:75","Qty:Float:100", "Transferred by:Data:140","Received by:Data:150","Recieved Date:Date:100" ], []
    # Date	Item	UOM	Qty
    conditions = ""
    if filters.get("item"):
        conditions += """ and i.item_code = "{item_code}" """
    if filters.get("from"):
        conditions += """ and f.date between DATE("{from}") and DATE("{to}")"""
    if filters.get("item_group"):
        conditions += """ and ii.item_group = "{item_group}" """
    if filters.get("production_order"):
        conditions += """ and f.production_order = "{production_order}" """

    data = frappe.db.sql("""SELECT f.name, f.date, p.name, p.expected_delivery_date, i.item_code,i.item_name,i.uom,i.qty, 
        f.transferred_by, f.received_by, f.received_date from `tabFinished Goods Transfer Item` i JOIN `tabFinished Goods Transfer Form` f 
        ON i.parent=f.name JOIN `tabItem` ii ON (ii.name = i.item_code) JOIN `tabProduction Order` p ON 
        (f.production_order = p.name) WHERE f.docstatus =1 {0} """.format(conditions.format(**filters)), as_list=1)

    return columns, data
