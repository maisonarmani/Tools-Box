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
        if filters.get('posting_from') and filters.get('posting_to'):
            conditions += ' and tabEC.posting_date  BETWEEN DATE(\'{0}\') and DATE(\'{1}\')' \
                .format(filters.get('posting_from'), filters.get('posting_to'))

        sql = '''select tabEC.name , tabEC.approval_status, tabEC.total_claimed_amount, tabEC.total_sanctioned_amount,
                    tabEC.posting_date, tabEC.employee,tabEC.employee_name,tabEC.company , c1.comment_by_fullname 
                    from `tabExpense Claim` as tabEC 
                    LEFT OUTER JOIN tabComment c1 ON c1.comment_docname =  tabEC.name WHERE c1.comment = 'Authorized' {0}'''

        frappe.errprint(sql.format(conditions))
        data = frappe.db.sql(sql.format(conditions), as_list =1)
        for item in data:
            item += frappe.db.sql("select comment_by_fullname from `tabComment` where comment_docname = '{0}'"
                                  "and comment='{1}' limit 1".format(item[0], "Authorized"), as_list=1)
        print data
