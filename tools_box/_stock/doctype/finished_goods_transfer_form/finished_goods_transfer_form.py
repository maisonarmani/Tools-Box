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

        if self._validate_fields():
            frappe.throw("Finished goods transfer form already created for " +self.production_order)

        if self.is_new():
            self.transferred_by = _get_employee_fullname(frappe.session.data.user)


    def _validate_fields(self):
        d = frappe.db.sql("SELECT name FROM `tab%s` WHERE production_order = '%s' and name != '%s'" % (self.doctype,
                                                                                       self.production_order, self.name))
        return len(d) > 0


    def on_change(self):
        if self.workflow_state == "Received":
            se = frappe.new_doc("Stock Entry")
            se.purpose = "Material Receipt"
            se.title = "Material Receipt"
            se.from_warehouse = ""
            se.production_order = self.production_order

            for index, value in enumerate(self.items):
                # Get items default warehouse
                cur_item = frappe.get_list(doctype="Item", filters={"name": value.item_code},
                                           fields=['default_warehouse', 'standard_rate'])
                if index == 0:
                    se.to_warehouse = cur_item[0].default_warehouse
                    #se.manufactured_qty = value.qty
                    #se.fg_completed_qty = value.qty

                if len(se.to_warehouse) <= 0:
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
                    cost_center=d_cost_center,
                    basic_rate=cur_item[0].standard_rate,
                    amount=cur_item[0].standard_rate * value.qty,
                    valuation_rate=cur_item[0].standard_rate
                )
                se.append('items', item)

            se.insert()
            se.submit()


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
                      .format(doc=doc.doctype, rd=utils.now_datetime(), rb=_get_employee_fullname(frappe.session.data.user), name=doc.name))


def _get_employee_fullname(user):
    employee = frappe.get_list(doctype="Employee",fields=["employee_name"],filters={"user_id":user})

    if employee:
        return employee[0].employee_name
    return None