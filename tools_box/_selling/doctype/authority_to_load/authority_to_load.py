# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document


class AuthoritytoLoad(Document):
    def validate(self):
        # Get the sales order under it and check to see if the authority to load flag is set
        if self.has_sales_order():
            res = frappe.get_all('Sales Order', filters={"atl": 1, "name": self.sales_order})
            if res:
                frappe.throw(_("Authority to load has previously been generated for this Sales order [{so}]".format(
                    so=self.name)))
            res = frappe.get_all('Authority to Load', filters={"sales_order": self.sales_order})
            if res and res[0].name != self.name:
                frappe.throw(_("Authority to load [{atl}] has previously been generated for this Sales order [{so}]".format(
                    so=self.name, atl=res[0].name)))



    def on_submit(self):
        if self.has_sales_order():
            # if the we have another authority to load that has been
            # submitted and has the specified sales order on it then throw and error
            res = frappe.get_all('Authority to Load', filters=[
                ["name", "!=", self.name],
                ["sales_order", "=", self.sales_order],
                ["docstatus", "=", 1]], fields=['name'])
            if res:
                frappe.throw(_("Authority to load has previously been generated for this Sales order [{so}]".format(
                    so=self.get_so_title())))
            frappe.db.sql(
                "update `tabSales Order` set atl=1 where name='{sales_order}'".format(sales_order=self.sales_order))

    def on_cancel(self):
        if self.has_sales_order():
            frappe.db.sql(
                "update `tabSales Order` set atl=0 where name='{sales_order}'".format(sales_order=self.sales_order))

    def on_trash(self):
        pass

    def on_error(self):
        frappe.errprint("Error occurred while saving...")

    def has_sales_order(self):
        return self.sales_order != ""

    def get_so_title(self):
        doc = frappe.get_all('Sales Order', fields=['title'], filters=[["name", "=", self.sales_order]],
                             ignore_permissions=True)
        return doc[0].title

@frappe.whitelist()
def make_authority_to_load(source_name, target_doc=None):
    from frappe.model.mapper import get_mapped_doc
    def set_missing_values(source, target):
        target.sales_order = source.name

    def update_item(source_doc, target_doc, source_parent):
        pass

    doc = get_mapped_doc("Sales Order", source_name, {
        "Sales Order": {
            "doctype": "Authority to Load",
            "validation": {
                "docstatus": ["=", 1]
            },
            "field_map": {
                "sales_order": "name"
            },
            "add_if_empty": False,
            "postprocess": update_item,
            "condition": lambda doc: doc.docstatus == 1
        },
    }, target_doc, set_missing_values)

    return doc