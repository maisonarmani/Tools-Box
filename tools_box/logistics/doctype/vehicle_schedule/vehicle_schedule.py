# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class VehicleSchedule(Document):
    def validate(self):
        for item in self.vehicle_schedule_outbound_item:
            i = frappe.get_list("Vehicle Schedule {type} Item".format(type=self.type),
                                [["ref_name", "=", item.ref_name], ["parent", "!=", self.name]])
            if len(i) > 0:
                frappe.throw("Reference name {ref} is already covered ".format(
                    ref=item.ref_name))

    def before_save(self):
        # required clean so we dont have duplicate data
        if self.type == "Inbound":
            self.vehicle_schedule_outbound_item = []
        else:
            self.vehicle_schedule_inbound_item = []


        if self.ratio_ok == 0 and self.is_new():
            self.status = "Awaiting Approval"

        elif self.ratio_ok == 1 and self.is_new():
            self.status = "Awaiting Purchase Order"



@frappe.whitelist(False)
def get_daily_cost(vehicle=None):
    if vehicle:
        daily_cost = frappe.get_list("Vehicle Daily Cost", filters={
            "vehicle": vehicle,
            "enabled": 1
        }, fields=['total_cost'])

        if not len(daily_cost):
            return 0
        else:
            return daily_cost[0].get('total_cost')
    return 0


@frappe.whitelist(False)
def get_party(doctype=None, docname=None):
    if doctype and docname:
        party = "supplier"
        if doctype == "Delivery Note":
            party = "customer"
        p = frappe.get_list(doctype, filters={
            "name": docname,
            "docstatus": 1
        }, fields=[party])

        if len(p):
            return p[0].get(party)
    return 0


@frappe.whitelist(False)
def get_allowed():
    ls = frappe.get_single("Logistics Settings")
    if ls:
        return dict(
            outbound=ls.get("allowed_outbound_cost"),
            inbound=ls.get("allowed_inbound_cost")
        )


@frappe.whitelist(False)
def deliver(dt,dn):
    #Hack
    frappe.db.sql("update `tab{dt} Outbound Item` set status = 'Delivered' where parent = '{dn}'".format(dt=dt, dn=dn))
    frappe.db.sql("update `tab{dt} Inbound Item` set status = 'Delivered' where parent = '{dn}'".format(dt=dt, dn=dn))


@frappe.whitelist(False)
def change_status(dt, dn, status):
    doc = frappe.get_doc(dt, dn)
    doc.status = status
    if status == "Declined" or status == "Completed":
        doc.docstatus = 1
    doc.save(ignore_permissions=1)


def update_status(document, trigger):
    # check the purchase order if it has a vehicle schedule stamp on it
    # after approving the purchase order the vehicle schedule is then change t
    if document.get('vehicle_schedule') and document.get('workflow_state') == "Approved":
        doc = frappe.get_doc("Vehicle Schedule", document.get('vehicle_schedule'))
        if doc:
            doc.status = "Completed"
            doc.docstatus = 1
            doc.save(ignore_permissions=1)



@frappe.whitelist()
def make_purchase_order(docname):
    def check_purchase_order():
        p = frappe.db.sql("""select name from `tabPurchase Order` where vehicle_schedule=%s""", vs.name)
        return p[0][0] if p else ""

    vs = frappe.get_doc("Vehicle Schedule", docname)
    po = check_purchase_order()
    if po:
        frappe.throw(_("Purchase Order {0} already exists for the Vehicle Schedule").format(po))

    po = frappe.new_doc("Purchase Order")
    po.supplier = vs.supplier
    po.vehicle_schedule = vs.name
    po.company="Graceco Limited"
    po.transaction_date = vs.date

    po.append("items", {
        "item_name":"Van Hire & Delivery Service",
        "description":"Van Hire & Delivery Service",
        "uom":"Nos",
        "stock_uom":"Nos",
        "schedule_date":vs.date,
        "item_code": "GCL0716",
        "unit_cost":vs.daily_cost,
        "rate":vs.daily_cost,
        "amount":vs.daily_cost,
        "qty":1,
        "conversion_factor":"1",
    })

    return po.as_dict()