# -*- coding: utf-8 -*-
# Copyright (c) 2015, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class StoreBinCard(Document):
    pass

@frappe.whitelist(False)
def get_items(doctype=None, docname=None):
    items = []
    if doctype is not None:
        if doctype == 'Stock Entry':
            child = "Stock Entry Detail"
            items = frappe.db.sql("""select c.item_code, c.qty qty ,c.uom , c.description, c.item_name from `tab{parent}` p , `tab{child}` c where (p.name = c.parent )
								  and p.name = '{name}' """.format(name=docname, parent=doctype, child=child),
                                  as_dict=1)

        elif doctype == 'Purchase Receipt':
            child = "Purchase Receipt Item"
            items = frappe.db.sql("""select c.item_code, c.qty qty ,c.uom , c.description, c.item_name from `tab{parent}` p , `tab{child}` c where (p.name = c.parent )
								  and p.name = '{name}' """.format(name=docname, parent=doctype, child=child),
                                  as_dict=1)

        elif doctype == 'Delivery Note':
            child = "Delivery Note Item"
            items = frappe.db.sql("""select c.item_code, abs(c.qty) qty ,c.uom , c.description, c.item_name from `tab{parent}` p , `tab{child}` c where (p.name = c.parent )
									and p.name = '{name}' """.format(name=docname, parent=doctype, child=child),
                                  as_dict=1)

    return items
