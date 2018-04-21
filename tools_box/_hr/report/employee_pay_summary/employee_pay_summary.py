# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
from tools_box._hr.report.employee_report_summary.employee_report_summary import EmployeeSummary
import frappe


def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data


def get_data(filters=None):
    conditions, data = "SELECT e.employee, e.employee_name, e.employment_type, s.total_earning, ss.base , e.date_of_joining, " \
                       "e.status  FROM `tabEmployee` e,`tabSalary Structure` s,`tabSalary Structure Employee` ss " \
                       "WHERE (ss.parent = s.name) and (e.employee = ss.employee) and  s.is_active = 'Yes' ", []

    if filters.get("status") and filters.get("status") != "All":
        conditions += " AND e.status = '%(status)s'"
    if filters.get("employment_type") and filters.get("employment_type") != 'All':
        conditions += " AND e.employment_type = '%(employment_type)s'"
    if filters.get("department"):
        conditions += " AND e.department = '%(department)s'"

    order_by = " ORDER BY e.employee_name,e.status ASC, s.creation ASC"

    if conditions:
        data = frappe.db.sql(conditions % filters + order_by, as_list=1)
        for datum in data:
            d_s = EmployeeSummary.get_number_of_days_spent_with_company(datum[0])
            if datum[3] == 0:
                datum [3] = datum[4]
            del datum[4]
            datum.append(d_s)
    return data


def get_columns(filters):
    column = [
        _("Employee ID") + ":Link/Employee:120",
        _("Name") + ":Data:200",
        _("Employment Type") + ":Data:150",
        _("Gross Pay") + ":Currency:130",
        _("Joined Date") + ":Date:130",
        _("Status") + ":Data:70",
        _("Been With Company ") + ":Data:190",
    ]

    if filters.get('status') == "Left":
        column.append(_("Relieving Date") + ":Date:130")
    return column
