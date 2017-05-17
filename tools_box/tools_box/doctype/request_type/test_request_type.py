# -*- coding: utf-8 -*-
# Copyright (c) 2015, bobzz.zone@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals

from datetime import date
import frappe
import unittest


# test_records = frappe.get_test_records('Request Type')

class TestRequestType(unittest.TestCase):
    def test(self):
        # date from, date to, warehouse , item and item group
        conditions = ""
        filters = dict(
            from_date=date(2014, 1, 1),
            to_date=date(2017, 03, 31),
            #warehouse='Princess Finished Goods - GCL',
            #item_group='Princess',
            #item_code='GCL0014',
        )

        if (filters.get("from_date") and filters.get("from_date")):
            conditions += " AND sle.posting_date <= '{to_date}'"
        else:
            frappe.throw(frappe._("From date and to date are required fields"))

        if filters.get("item_code"):
            conditions += " AND sle.item_code = \"{item_code}\""
        if filters.get("warehouse"):
            conditions += " AND sle.warehouse = \"{warehouse}\""
        if filters.get("item_group"):
            conditions += " AND item.item_group = \"{item_group}\""

        ''' go thru all items in warehouse
        then go to the stock ledger entry and see what is left of that '''
        query = '''SELECT sle.item_code ,item.item_name, item.item_group, sle.posting_date, sle.qty_after_transaction
					FROM `tabStock Ledger Entry` sle LEFT OUTER JOIN `tabItem` item ON (item.item_code = sle.item_code)
					WHERE sle.voucher_type = "Stock Entry" AND sle.docstatus < 2 {conds} ORDER BY sle.item_code ,sle.posting_date ,sle.posting_time
			'''
        data = frappe.db.sql(query.format(conds=conditions).format(**filters))
        print(query.format(conds=conditions).format(**filters))
        data_redefined, c = [], 1
        for datum in data:
            try:
                if data[c][0] != datum[0]:
                    data_redefined.append(datum);
            except IndexError as err:
                data_redefined.append(datum)
            c += 1

        print(data_redefined.__len__())
        print(data_redefined)