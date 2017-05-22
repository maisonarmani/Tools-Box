# -*- coding: utf-8 -*-
# Copyright (c) 2015, bobzz.zone@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest


# test_records = frappe.get_test_records('Petty Cash Log')

class TestPettyCashLog(unittest.TestCase):
    def test_get_authorizer(self):
        filters = {
            "posting_from": "2016-01-12",
            "posting_to": "2017-01-12"
        }

        conditions = ""
        if filters.get("from_date"):
            conditions += " AND d.expense_date >= %(from_date)s"
        if filters.get("to_date"):
            conditions += " AND d.expense_date <= %(to_date)s"
        if filters.get("approver"):
            conditions += " AND p.exp_approver = %(approver)s"
        if filters.get("expense_type"):
            conditions += " AND d.expense_type = %(expense_type)s"

        data = frappe.db.sql(
            "SELECT d.expense_date,p.name,d.expense_type,d.description,d.sanctioned_amount,p.exp_approver, c.comment_by FROM "
            "`tabExpense Claim` p LEFT JOIN `tabExpense Claim Detail` d ON (p.name = d.parent) LEFT OUTER JOIN tabComment c"
            " ON (p.name = c.comment_docname) and c.comment = 'Authorized' WHERE p.docstatus=1 {0}"
                .format(conditions), filters, as_list=1)

        print data
