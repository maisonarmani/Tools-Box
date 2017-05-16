# Copyright (c) 2013, Maison Armani Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from  sets import ImmutableSet
import frappe


def execute(filters={}):
    return get_columns(), get_data(filters)


def get_data(filters={}):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND si.posting_date >= DATE(\"%(from_date)s\")"
    if filters.get("to_date"):
        conditions += " AND si.posting_date <= DATE(\"%(to_date)s\")"
    if filters.get("customer"):
        conditions += " AND si.customer = \"%(customer)s\""
    if filters.get("item_group"):
        conditions += " AND sii.item_group = \"%(item_group)s\""

    query = """
          SELECT si.customer,SUM(sii.qty), SUM(sii.base_amount) FROM `tabSales Invoice` si, `tabSales Invoice Item` sii
          WHERE si.name = sii.parent {0} GROUP BY si.customer ORDER BY si.customer, si.posting_date""".\
                format(conditions) % filters

    data, data_n = frappe.db.sql(query, as_list=True), []

    for datum in data:
        datum += list(get_commission(filters.get('item_group'), datum[1], datum[2]))
        data_n.append(tuple(datum))
        datum = []

    return data_n


def get_columns():
    return [
        "Customer:Link/Customer:300",
        "Total Quantity:Float:100",
        "Total Amount:Currency:100",
        "Commission (%):Float:100",
        "Commission:Currency:100"
    ]


def get_commission(brand="Princess", qty=0, base_amount=0):
    if brand == "Princess":
        if qty >= 100 and qty < 1000:
            return [2, (2.0 /100.0) * base_amount]
        elif qty >= 1000 and qty < 2000:
            return [2.5, (2.5 / 100.0) * base_amount]
        elif qty >= 2000 and qty < 3000:
            return [3, (3.0 / 100.0) * base_amount]
        elif qty >= 3000 and qty < 4000:
            return [3.5, (3.5 / 100.0) * base_amount]
        elif qty >= 4000:
            return [4, (4.0 / 100.0) * base_amount]
        else:
            return [0.0, 0.0]
    else:
        return [0, 0]
