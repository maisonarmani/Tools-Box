# -*- coding: utf-8 -*-
# Copyright (c) 2016, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from tools_box._stock.doctype.finished_goods_transfer_form.finished_goods_transfer_form import _get_employee_fullname


class RawMaterialsReturnForm(Document):
    def validate(self):
        if self.is_new():
            self.returned_by = _get_employee_fullname(frappe.session.data.user)

    def _validate_fields(self):
        d = frappe.db.sql("SELECT name FROM `tab%s` WHERE production_order = '%s' and name != '%s'" % (self.doctype,
                                                                                                       self.production_order,
                                                                                                       self.name))
        return len(d) > 0

    def on_change(self):
        if self.workflow_state == "Completed":
            update_production_order(self.production_order, "Completed")


        if self.workflow_state == "Received":
            # do a transfer instead
            # get the wip warehouse from the production order
            nmrf = frappe.new_doc("Stock Entry")
            nmrf.purpose = "Material Transfer"
            nmrf.title = "Raw Material Return from ".format(self.production_order)
            nmrf.from_warehouse = get_wip(self.production_order)

            nmrf.production_order = self.production_order

            for index, value in enumerate(self.items):
                # Get items default warehouse
                cur_item = frappe.get_list(doctype="Item", filters={"name": value.item_code},
                                           fields=['default_warehouse'])

                if index == 0:
                    nmrf.to_warehouse = cur_item[0].default_warehouse

                if nmrf.to_warehouse == "":
                    frappe.throw("Item {0} does not have default warehouse required for material transsfer".format(
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
            update_me(self.name, nmrf.name, self.production_order)


def update_me(me, se, po):
    try:
        frappe.db.sql(
            "UPDATE `tabRaw Materials Return Form` SET stock_entry = '{0}' WHERE name = '{1}'".format(se, me))

        # stamp raw material form on production order
        frappe.db.sql(
            "UPDATE `tabProduction Order` SET has_raw_returned = 1, raw_material_return = '{0}' WHERE name = '{1}'"
                .format(me, po))

    except Exception as e:
        return False


def get_wip(name):
    _ = frappe.db.sql("SELECT wip_warehouse FROM `tabProduction Order` WHERE name = '%s'" % name , as_dict=1)
    if len(_):
        return _[0].wip_warehouse

    return  ""


def update_production_order(name,status):
    _ = frappe.db.sql("SELECT qty, produced_qty FROM `tabProduction Order` WHERE name = '%s' AND status != 'Stopped' "
                      % name, as_dict=1)
    if len(_) and (_[0].qty < _[0].produced_qty):
        frappe.errprint("Production Manufactured Quantity is less than expected quantity, "
                        "Sorry you have to continue the production or manually stop it.")

    else:
        frappe.db.sql("UPDATE `tabProduction Order` SET status = '%s', docstatus =1 WHERE name = '%s' AND status != 'Stopped'"
              % (status, name))

@frappe.whitelist(False)
def get_production_items(production_order=None):
    if production_order != None:
        # get the stock entry record for the particular production order
        stock_entry = frappe.get_list(doctype="Stock Entry", filters={
            "production_order": production_order,
            "purpose": "Material Transfer for Manufacture"
        }, fields=['name'])

        if stock_entry[0].get('name') != None:
            stock_entry_details = frappe.get_list(doctype="Stock Entry Detail", filters={
                "parent": stock_entry[0].get('name')
            }, fields=['item_code', 'item_name', 'qty', 'uom'])
