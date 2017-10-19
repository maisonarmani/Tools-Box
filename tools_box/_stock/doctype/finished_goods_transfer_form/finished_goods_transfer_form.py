# -*- coding: utf-8 -*-
# Copyright (c) 2015, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import utils
import traceback

class FinishedGoodsTransferForm(Document):
    def validate(self):
        if self.is_new():
            self.transferred_by = frappe.session.data.full_name

    def on_change(self):
        if self.workflow_state == "Approved":
            nmrf = frappe.new_doc("Stock Entry")
            nmrf.purpose = "Material Receipt"
            nmrf.title = "Material Receipt"
            nmrf.from_warehouse = ""
            nmrf.production_order = self.production_order

            for index, value in enumerate(self.items):
                # Get items default warehouse
                cur_item = frappe.get_list(doctype="Item", filters={"name": value.item_code},
                                           fields=['default_warehouse'])
                if index == 0:
                    nmrf.to_warehouse = cur_item[0].default_warehouse
                    # nmrf.manufactured_qty = value.qty,

                if len(nmrf.to_warehouse) <= 0:
                    frappe.throw("Item {0} does not have default warehouse required for stock entry".format(
                        value.item_code))

                # using the latest cost center for item
                last_cost_center = frappe.get_list(doctype="Stock Entry Detail",
                                                   filters={"item_code": value.item_code}, fields=['cost_center'],
                                                   order_by='creation')

                d_cost_center = ""
                if last_cost_center[0].get('cost_center') != None:
                    d_cost_center = last_cost_center[0].cost_center

                # set new item
                item = dict(
                    t_warehouse=cur_item[0].default_warehouse,
                    qty=value.qty,
                    item_code=value.item_code,
                    item_name=value.item_name,
                    uom=value.uom,
                    cost_center=d_cost_center
                )
                nmrf.append('items', item)

            nmrf.insert()
            nmrf.submit()


@frappe.whitelist(False)
def get_producted_items(production_order=None):
    if production_order != None:
        prod = frappe.get_list(doctype="Production Order", filters={
            "name": production_order,
        }, fields=['production_item as item_code', 'qty'])

        for itm in prod:
            item = frappe.get_list(doctype="Item", filters={
                "name": itm.item_code,
            }, fields=['item_name', 'stock_uom as uom'])
            itm.update(item[0])
        return prod
    return []

@frappe.whitelist(False)
def update_receivers(doc, trigger):
    if doc.workflow_state == "Received":
        frappe.db.sql("update `tab{doc}` set received_date = '{rd}',received_by ='{rb}' where name = '{name}'"
                      .format(doc=doc.doctype, rd=utils.now_datetime(), rb=frappe.session.user_fullname, name=doc.name))
