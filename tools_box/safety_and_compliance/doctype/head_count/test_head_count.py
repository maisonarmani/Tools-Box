# -*- coding: utf-8 -*-
# Copyright (c) 2015, bobzz.zone@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals
import frappe
import unittest


# test_records = frappe.get_test_records('Head Count')

class TestHeadCount(unittest.TestCase):
    def test_leave(self):
        for leave_type in frappe.db.sql('''select name from `tabLeave Type`''', as_list=True):
            print(leave_type[0])
            leave = frappe.db.get_list('Leave Allocation', fields=["total_leaves_allocated", "employee_name"],
                                     filters=[["leave_type", "=", leave_type[0]]])
            #print(leave)


def unknown(self):
    # import inspect
    # print(inspect.getargspec(frappe.get_all))
    import datetime
    date = datetime.datetime(2017, 11, 02)
    print(
        frappe.get_all("Head Count", fields=[
            "name", 'modified'
        ], filters={"modified": (">=", date)}, order_by="modified", limit_page_length=1, limit_page_start=0)
    )


def unsent_email(self):
    # get_unsent_emails()
    pass
