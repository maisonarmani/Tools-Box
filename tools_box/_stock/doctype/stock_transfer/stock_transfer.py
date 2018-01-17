# -*- coding: utf-8 -*-
# Copyright (c) 2018, Convergenix and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry


class StockTransfer(Document):
    def on_submit(self):
        # perform a stock transfer
        # including the location of the warehouse
        '''Helper function to make a Stock Entry
            :item_code: Item to be moved
            :qty: Qty to be moved
            :from_warehouse: Optional
            :to_warehouse: Optional
            :rate: Optional
            :serial_no: Optional
            :batch_no: Optional
            :posting_date: Optional
            :posting_time: Optional
            :do_not_save: Optional flag
            :do_not_submit: Optional flag
            '''
        for item in self.stock_transfer_item:
            make_stock_entry(item_code=item.item_code, qty=item.quantity, from_warehouse=item.default_warehouse,
                             to_warehouse=self.destination_warehouse, posting_date=self.transfer_date,
                             location=self.location)


from frappe import _
@frappe.whitelist()
def make_way_bill(docname):
    def check_wb(docname):
        p = frappe.db.sql("""select name from `tabWay Bill` where stock_transfer='%s'""" % docname)
        return p[0][0] if p else ""

    st = frappe.get_doc("Stock Transfer", docname)
    if check_wb(docname):
        frappe.throw(_("Way Bill {0} already exists for the Stock Transfer").format(docname))

    wb = frappe.new_doc("Way Bill")
    wb.stock_transfer = st.name
    wb.from_loc = "Head Office"
    wb.to_loc = st.location

    wb.company = st.company

    for i, item in enumerate(st.stock_transfer_item):
        if i is 0:
            wb.net_weight_uom = item.item_uom

        it = frappe.new_doc("Packing Slip Item")
        it.set('qty',item.quantity)
        it.set('stock_uom',item.item_uom)
        it.set('item_code',item.item_code)
        it.set('item_name',item.item_name)
        wb.append("items", it)
    return wb.as_dict()
