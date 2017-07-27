# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns = [
        _("Item") + ":Link/Item:100",
        _("Item Name") + "::130",
        _("Item Group") + ":Item Group:130",
        _("Warehouse") + ":Link/Warehouse:120",
        _("Date") + ":Datetime:120",
        _("Balance Qty") + ":Float:40",
    ]

    data, conditions = [], ""

    if (filters.get("as_at_date")):
        conditions += " AND sle.posting_date <= DATE_ADD('{as_at_date}', INTERVAL 1 DAY)"
    else:
        frappe.throw(frappe._("As at date is a required field"))

    if filters.get("item_code"):
        conditions += " AND sle.item_code = \"{item_code}\""
    if filters.get("warehouse"):
        conditions += " AND sle.warehouse = \"{warehouse}\""
    if filters.get("item_group"):
        conditions += " AND item.item_group = \"{item_group}\""

    ''' go thru all items in warehouse
    then go to the stock ledger entry and see what is left of that '''
    query = '''SELECT sle.item_code ,item.item_name, item.item_group,sle.warehouse,  sle.posting_date, sle.
            qty_after_transaction FROM `tabStock Ledger Entry` sle LEFT OUTER JOIN `tabItem` item ON 
            (item.item_code = sle.item_code) WHERE sle.voucher_type = "Stock Entry" AND sle.docstatus < 2 {conds} 
            ORDER BY sle.item_code ,sle.posting_date ,sle.posting_time
    			'''
    data = frappe.db.sql(query.format(conds=conditions).format(**filters))
    data_redefined, c = [], 1
    for datum in data:
        try:
            if data[c][0] != datum[0]:
                data_redefined.append(datum);
        except IndexError as err:
            data_redefined.append(datum)
        c += 1

    return columns, tuple(data_redefined)
