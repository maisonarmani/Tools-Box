# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class PurchaseRequisition(Document):

    def before_save(self):
        if self.budgeted_expense == 0 and self.is_new():
            self.status = "Awaiting Clearance"

    def on_change(self):
        roles = frappe.get_roles(frappe.session.get('user'))
        if self.status == "Approved":
            if "Financial Controller" not in roles:
                c_employee = frappe.get_value("Employee", {"user_id": frappe.session.get('user') }, "name")
                if self.approved_by != c_employee:
                    frappe.throw("Sorry, this document can only be approved by the financial controller and %s" %
                                 self.approved_by)

        if self.status == "Authorized":
            c_employee = frappe.get_value("Employee", {"user_id": frappe.session.get('user') }, "name")
            if self.authorized_by != c_employee:
                frappe.throw("Sorry, this document can only be authorized by and %s" %
                             self.authorized_by)






@frappe.whitelist()
def make_purchase_order(docname):
    def check_purchase_order():
        p = frappe.db.sql("""select name from `tabPurchase Order` where purchase_requisition='%s'""" % pr.name)
        return p[0][0] if p else ""

    pr = frappe.get_doc("Purchase Requisition", docname)
    po = check_purchase_order()
    if po:
        frappe.throw(_("Purchase Order {0} already exists for the Purchase Requisition").format(po))

    po = frappe.new_doc("Purchase Order")
    po.purchase_requisition = pr.name
    po.company = pr.company
    po.transaction_date = pr.date
    po.currency = pr.currency


    for item in pr.items:
        item.base_net_amount = item.amount
        item.net_amount = item.amount
        item.net_rate = item.rate
        item.amount = item.rate
        item.docstatus =0
        po.append("items", item)

    return po.as_dict()
