# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    data = []
    columns = [
        "Item By:Link/Item:100",
        "Item Name:Data:200",
        "Supplier:Link/Supplier:130",
        "Rate:Currency:130",
        "Last Updated:Date:200",
    ]

    if filters.get("item"):
        purchase_items = [dict(name=filters.get("item"))]
    else:
        # select * purchase items
        purchase_items = "SELECT name from `tabItem` where is_purchase_item=1"
        purchase_items = frappe.db.sql(purchase_items, as_dict=1)

    condtions = ""
    if filters.get('supplier'):
        condtions += " AND p.supplier = '%s'" % filters.get('supplier')

    for item in purchase_items:
        frappe.errprint(item)
        sql = "SELECT c.item_code, c.item_name, p.supplier, c.rate, p.creation as last_update FROM " \
              "`tabPurchase Order` p INNER JOIN `tabPurchase Order Item` c ON (p.name = c.parent) WHERE (c.item_code = '%s')" \
              " %s ORDER BY p.creation DESC LIMIT 1" % (item.get('name'),condtions)

        d = frappe.db.sql(sql)
        if d != ():
            data.append(d[0])

    return columns, data
