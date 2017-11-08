# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry


class StationariesRequest(Document):
    def on_change(self):

        # identify the warehouse that has enough in stock
        # check the quantity requested and see all we have in store
        # then transfer req quantity from the warehouse to the stationaries warehouse
        # then submit

        # we also need the warehouse with the largest stock quantity of
        if self.workflow_state == "Received":
            for item in self.items:
                xi = _get_max_warehouse(item.item)
                if xi != 0:
                    make_stock_entry(
                        item_code=item.item,
                        from_warehouse=xi,
                        to_warehouse="Stationaries - GCL",
                        qty=item.qty
                    )
                    _update_receiver(self)
                    _create_bin_card(item, self)
                else:
                    frappe.throw(
                        "Ooops... {0} - {1} is not available in other warehouses.".format(item.item_name, item.item))
        elif self.workflow_state == "Approved":
            _update_approver(self)


def _update_approver(doc):
    frappe.db.sql("update `tab{doc}` set approved_by = '{rd}',approved_by_name ='{rb}' where name = '{name}'"
                  .format(doc=doc.doctype, rd=frappe.session.data.user,
                          rb=_get_employee_fullname(frappe.session.data.user), name=doc.name))


def _update_receiver(doc):
    frappe.db.sql("update `tab{doc}` set received_by = '{rd}',received_by_name ='{rb}' where name = '{name}'"
                  .format(doc=doc.doctype, rd=frappe.session.data.user,
                          rb=_get_employee_fullname(frappe.session.data.user), name=doc.name))


def _get_employee_fullname(user):
    employee = frappe.get_list(doctype="Employee", fields=["employee_name"], filters={"user_id": user})

    if employee:
        return employee[0].employee_name
    return None


def _get_max_warehouse(item):
    warehouse = frappe.db.sql("select warehouse, SUM(actual_qty)  from `tabStock Ledger Entry` where "
                              "item_code = '{item}'  and warehouse != 'Stationaries - GCL' "
                              "GROUP BY warehouse ORDER BY actual_qty DESC LIMIT 1".format(item=item))
    if warehouse is not []:
        if warehouse[0][1] > 0:
            return warehouse[0][0]
    return 0


def _create_bin_card(item, doc):
    import datetime

    last_value = _last_bin_card_value(item)

    new_bin_card = frappe.new_doc("Stationaries Bin Card")
    new_bin_card.date = datetime.datetime.today()
    new_bin_card.item = item.item
    new_bin_card.value = item.pqty
    new_bin_card.current_value = last_value[0] + item.pqty
    new_bin_card.last_value = last_value[0]
    new_bin_card.reference_doctype = doc.doctype
    new_bin_card.reference_docname = doc.name
    new_bin_card.ppu = last_value[1]
    new_bin_card.count =  last_value[0]

    new_bin_card.submit()


def _last_bin_card_value(item):
    last_value = frappe.db.sql("SELECT current_value,ppu, count FROM `tabStationaries Bin Card`  where item = '{item}'  "
                               "ORDER BY date DESC LIMIT 1".format(item=item.item))

    if len(last_value):
        return last_value[0]
    return [0,item.ppu,0]
