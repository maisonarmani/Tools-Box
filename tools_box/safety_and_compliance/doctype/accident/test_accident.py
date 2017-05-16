# -*- coding: utf-8 -*-
# Copyright (c) 2015, masonarmani38@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals
from datetime import datetime, date
from frappe import _

import frappe
import unittest

from erpnext.hr.doctype.leave_application.leave_application \
    import get_leave_allocation_records, get_leave_balance_on, get_approved_leaves_for_period


# test_records = frappe.get_test_records('Accident Report Form')

class TestAccidentReportForm(unittest.TestCase):
    def tt_get_employee_experience(self):
        employee_id = "GCL-EMP/0089"
        employee, experience = [], []
        if employee_id:
            employee = frappe.get_doc('Employee', employee_id)
            if employee:
                experience = {
                    'internal': employee.internal_work_history,
                    'external': employee.external_work_history
                }

    def tt_standard(self):

        '''frappe.sendmail(
            recipients= ['masonarmani38@gmail.com','masonarmani38@outlook.com'],
            as_markdown=False,
            content="Hello People",
            message="Maison Armani is testing this guy but what can i say",
            subject="Maison Armani"
        )
        frappe.get_list("Employee")
        '''
        printed = ""
        frappe.set_user("ese.egbevwie@graceco.com.ng")  # Simulate login user
        printed = frappe.as_json(
            frappe.get_all("Employee", fields="*", filters=[["modified_by", "=", "Administrator"]], limit_page_length=1,
                           order_by='modified asc'), )
        frappe.has_permission(doctype="Employee", ptype=('cancel'), throw=False)

    def tt_employee_status(self):
        ## Test
        filters = dict(
            from_date=datetime(2016, 01, 01),
            to_date=datetime(2016, 12, 01),
            status="Left",
            employment_type="Full-time"
        )
        conditions, data = "SELECT employee, employee_name, employment_type, date_of_joining, status ,relieving_date FROM `tabEmployee` WHERE (1=1)", []
        date_type = "date_of_joining"

        if filters.get("status") == "Left": date_type = "relieving_date"
        if filters.get("from_date"):
            conditions += " AND {dt} >= '%(from_date)s'".format(dt=date_type)
        if filters.get("to_date"):
            conditions += " AND {dt} <= '%(to_date)s'".format(dt=date_type)
        if filters.get("status") and filters.get("status") != "All":
            conditions += " AND status = '%(status)s'"
        if filters.get("employment_type") and filters.get("employment_type") != 'All':
            conditions += " AND employment_type = '%(employment_type)s'"

        frappe.errprint(conditions % filters)

        misc = " ORDER BY employee_name,status ASC"
        if conditions:
            data = frappe.db.sql(conditions % filters + misc)
        return data

    def tes1_get_data(self):
        filters = dict(
            from_date=datetime(2016, 01, 01),
            to_date=datetime(2016, 12, 01),
            gender="Female",
            employment_type="Full-time",
            leave_type="Annual",
            department=""
        )
        self.get_record(filters)

    def get_days_spent(self, employee):
        # days spent in company
        data = frappe.db.sql("SELECT date_of_joining from `tabEmployee` WHERE  name = '{name}'".format(name=employee))
        __date__ = date.today() - data[0][0]
        months, days = 0, 0
        years = __date__.days / 365
        if __date__.days % 365 > 0:
            months = __date__.days % 365 / 31
        if __date__.days % 365 % 31 > 0:
            days = __date__.days % 365 % 31

        return {"Years": years, "Months": months, "Days": days}

    def get_record(self, filters):
        allocation_records_based_on_to_date = get_leave_allocation_records(filters.get('to_date'))
        data, active_employees = [], frappe.get_all("Employee", filters={"status": "Active"},
                                                    fields=["name", "employee_name", "department"])
        for employee in active_employees:
            row = [employee.name, employee.employee_name, employee.department, self.get_days_spent(employee.name)]
            # if leave type is selected in the filter
            # leaves taken
            leaves_taken = get_approved_leaves_for_period(employee.name,
                                                          filters.get('leave_type'), filters.get('from_date'),
                                                          filters.get('to_date'))
            # closing balance
            closing = get_leave_balance_on(employee.name,
                                           filters.get('leave_type'), filters.get('to_date'),
                                           allocation_records_based_on_to_date.get(employee.name, frappe._dict()))

            row += [leaves_taken, closing]
            data.append(row)

        print(data)
