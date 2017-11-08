# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class StationariesLog(Document):
    def on_submit(self):
        for item in self.items_issued:
            _create_bin_card(item, self)


def _create_bin_card(item, doc):
    import datetime

    last_value = _last_bin_card_value(item)
    if last_value[0] < 0:
        frappe.throw("No more ")
    new_bin_card = frappe.new_doc("Stationaries Bin Card")
    new_bin_card.date = datetime.datetime.today()
    new_bin_card.item = item.item_issued
    new_bin_card.value = item.pqty

    new_bin_card.current_value = last_value[0] + item.pqty
    new_bin_card.last_value = last_value[2]
    new_bin_card.reference_doctype = doc.doctype
    new_bin_card.reference_docname = doc.name
    new_bin_card.ppu = last_value[1]
    new_bin_card.count = last_value[0] + item.pqty

    less = new_bin_card.count
    if less >= new_bin_card.ppu: # count and current has to change
        unit = int(less / new_bin_card.ppu)
        if (less / new_bin_card.ppu) > 1:
            new_count = less % new_bin_card.ppu
        else:
            new_count = less - new_bin_card.ppu

        # set new values
        new_bin_card.count = new_count
        new_bin_card.current_value = new_count

        # set item values
        item.qty = unit
        item.ppu = new_bin_card.ppu

        # remove value from stock
        _remove_unit(item)

    new_bin_card.submit()

def _remove_unit(item):
    wh = "Stationaries - GCL"
    se = frappe.new_doc("Stock Entry")
    se.purpose = "Material Issue"
    se.title = "Material Issue"
    se.from_warehouse = wh

    # using the latest cost center for item
    last_cost_center = frappe.get_list(doctype="Stock Entry Detail",
                                       filters={"item_code": item.item_issued}, fields=['cost_center'],
                                       order_by='creation')

    d_cost_center = ""
    if last_cost_center[0].get('cost_center') != None:
        d_cost_center = last_cost_center[0].cost_center

    it = frappe.get_list(doctype="Item", filters={"name": item.item_issued},
                         fields=['stock_uom, item_name'])

    # set new item
    item = dict(
        f_warehouse=wh,
        t_warehouse="",
        qty=item.qty,
        item_code=item.item_issued,
        item_name=it[0].item_name,
        uom=it[0].stock_uom,
        cost_center=d_cost_center
    )

    se.append('items', item)
    se.submit()


def _last_bin_card_value(item):
    last_value = frappe.db.sql("SELECT `count`, ppu, current_value FROM `tabStationaries Bin Card` where item = '{item}'  "
                               "ORDER BY date DESC LIMIT 1".format(item=item.item_issued))

    if len(last_value):
        return last_value[0]
    return [0, item.ppu, 0]
