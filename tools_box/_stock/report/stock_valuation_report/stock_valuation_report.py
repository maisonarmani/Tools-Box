# Copyright (c) 2015, masonarmani38@gmail.com. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cint, getdate


def execute(filters=None):
    if not filters: filters = {}

    columns = get_columns()
    data = []

    conditions = "posting_date BETWEEN DATE('{0}') AND DATE('{1}')".format(filters.get('from_date'),
                                                                           filters.get('to_date'))

    if filters.get('warehouse'):
        conditions += " AND warehouse ='{0}'".format(filters.get('warehouse'))

    # get all active items and get last valuation rate
    items = frappe.db.sql("SELECT name, item_name, item_group, brand, description , stock_uom FROM `tabItem` "
                          "WHERE disabled = 0", as_dict=1)
    for item in items:
        sle = frappe.db.sql(
            "SELECT name, valuation_rate, company, warehouse FROM `tabStock Ledger Entry` "
            "WHERE item_code = '{0}' AND {1} ORDER BY posting_date DESC  LIMIT 1 ".format(item.name, conditions),
            as_dict=1)

    if sle:
        mp = (
            item.name, item.item_name, item.item_group, item.description, sle[0].get('warehouse'),
            item.stock_uom, sle[0].get('valuation_rate'), sle[0].get('name'), sle[0].get('company'),
        )
    data.append(mp)

    return columns, data


def get_columns():
    """return columns"""
    columns = [
        _("Item") + ":Link/Item:100",
        _("Item Name") + "::150",
        _("Item Group") + "::100",
        _("Description") + "::170",
        _("Warehouse") + ":Link/Warehouse:100",
        _("Stock UOM") + ":Link/UOM:90",
        _("Valuation Rate") + ":Float:90",
        _("Last Stock Ledger Entry") + ":Link/Stock Ledger Entry:120",
        _("Company") + ":Link/Company:100"
    ]

    return columns
