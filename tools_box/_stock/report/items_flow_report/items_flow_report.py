# Copyright (c) 2015, masonarmani38@gmail.com. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cint, getdate


def execute(filters=None):
    # get all items and see it movement trends from
    # for sales delivery note
    # for production check manufacture stock ledger and excess too
    # for purchase check purchase reciept

    columns, data = get_columns(), []
    items = get_all_items(filters.get('sales_item_only'), filters.get('warehouse'))

    period_start, period_end = filters.get('from'), filters.get('to')

    for item in items:
        sold = get_qa('Delivery Note', item.name, period_start, period_end)[0]
        man = get_qa('Stock Entry', item.name, period_start, period_end)[0]
        pur = get_qa('Purchase Receipt', item.name, period_start, period_end)[0]
        data.append([item.name, item.item_name, sold.get('qty'), sold.get('amt'), man.get('qty'), man.get('amt'),
                     pur.get('qty'), pur.get('amt')])

    return columns, data


def get_qa(parent, item_name, period_start, period_end):
    cond = ""
    if parent == 'Stock Entry':
        cond += "AND c.t_warehouse != ''"
        p, c = "tab" + parent, 'tab%s Detail' % parent
    else:
        p, c = "tab" + parent, 'tab%s Item' % parent

    return frappe.db.sql(
        "SELECT SUM(c.qty) qty, SUM(c.amount) amt FROM `%s` p, `%s` c "
        "WHERE  c.parent = p.name  AND  p.docstatus = 1 AND c.item_code = '%s' %s AND p.posting_date BETWEEN DATE('%s') "
        "AND DATE('%s') GROUP BY c.item_code, c.uom " % (p, c, item_name, cond, period_start, period_end), as_dict=1) or [{}]


def get_all_items(sales_item_only, warehouse):
    cond = ""
    if warehouse:
        cond += " AND default_warehouse = '%s'" % warehouse
    if sales_item_only:
        return frappe.db.sql(
            "SELECT name,item_name  FROM `tabItem` WHERE is_sales_item = 1 AND disabled = 0 %s " % cond,
            as_dict=1)
    else:
        return frappe.db.sql("SELECT name,item_name FROM `tabItem` WHERE disabled = 0 %s " % cond, as_dict=1)


def get_columns():
    """return columns"""
    columns = [
        _("Item") + ":Link/Item:100",
        _("Item Name") + ":Data:150",
        _("Quantity Sold") + ":Float:100",
        _("Amount Sold") + ":Currency:100",
        _("Quantity Produced") + ":Float:100",
        _("Amount Produced") + ":Currency:100",
        _("Quantity Purchased") + ":Float:100",
        _("Amount Purchased") + ":Currency:100",
    ]

    return columns
