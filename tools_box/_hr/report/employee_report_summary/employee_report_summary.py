# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
from datetime import datetime, date
import frappe


def execute(filters=None):
    employee_summary = EmployeeSummary
    data, columns = get_data(employee_summary, filters), get_columns(employee_summary, filters)
    return columns, data


def get_data(employee_summary, filters=None):
    conditions, data = "SELECT employee, employee_name, employment_type,department, gender FROM `tabEmployee` " \
                       "WHERE status = 'Active'", []
    '''
    date_type = "date_of_joining"
    if filters.get("from_date"):
        conditions += " AND {dt} >= '%(from_date)s'".format(dt=date_type)
    if filters.get("to_date"):
        conditions += " AND {dt} <= '%(to_date)s'".format(dt=date_type)
    '''
    if filters.get("gender") and filters.get("gender") != "All":
        conditions += " AND gender = '%(gender)s'"
    if filters.get("department") and filters.get("department") != "All":
        conditions += " AND department = '%(department)s'"
    if filters.get("employment_type"):
        conditions += " AND employment_type = '%(employment_type)s'"

    leave_type = filters.get("leave_type")

    frappe.errprint(conditions % filters)
    misc = " ORDER BY employee_name,status ASC"

    if conditions:
        data = frappe.db.sql(conditions % filters + misc, as_list=True)
        # for every employee row add additional information
        for datum in data:
            employee = datum[0]
            datum.append(employee_summary.get_number_of_days_spent_with_company(employee))
            for key, val in employee_summary.get_seperated_leave(employee, True, leave_type).items():
                datum.append(val)
    return data


def get_columns(employee_summary, filters):
    column = [
        _("Employee ID") + ":Link/Employee:120",
        _("Name") + ":Data:200",
        _("Employment Type") + ":Data:150",
        _("Department") + ":Data:150",
        _("Gender") + ":Data:150",
        _("Been With Company ") + ":Data:190"
    ]
    return column + employee_summary.additional_columns


class EmployeeSummary():
    additional_columns = []

    @classmethod
    def get_number_of_days_spent_with_company(cls, employee):
        employee = frappe.db.sql(
            '''select date_of_joining from `tabEmployee` where name = '{emp}' '''.format(emp=employee), as_list=1)
        doj = employee[0][0]  # date of joinig
        d0 = date(doj.year, doj.month, doj.day)
        d1 = date.today()
        delta = (d1 - d0)
        years, months, days = 0, 0, 0
        years = (delta.days / 365)
        days = (delta.days % 365)
        if days > 29:
            months = days / 29
            days = days % 29
        return "{yrs} Years {mnt} Months {dys} Days".format(yrs=years, mnt=months, dys=days)

    @classmethod
    def get_approved_leave(cls, employee, leave_type=None, from_date=None, to_date=None):
        date_filter, leave_type_filter = "", ""
        if to_date and from_date:
            date_filter = " and modified between DATE('{fd}') and DATE('{td}')".format(fd=from_date, td=to_date)
        if leave_type:
            leave_type_filter = " and name='{lt}'".format(lt=leave_type)

        # get approved leave
        approved_leave = {}
        for leave_type in frappe.db.sql(
                '''select name from `tabLeave Type` where (1=1) {ltf}'''.format(ltf=leave_type_filter), as_list=True):
            approved_leave.setdefault(leave_type[0], [])
            leave = frappe.db.sql(
                "select name, SUM(`total_leave_days`) from `tabLeave Application` where employee = '{employee}' and leave_type = '{lt}'"
                " {date_filter} and docstatus = 1".format(employee=employee, lt=leave_type[0], date_filter=date_filter),
                as_list=True)
            approved_leave[leave_type[0]] = leave

        return approved_leave

    @classmethod
    def get_allocated_leave(cls, employee, leave_type=None, from_date=None, to_date=None):
        date_filter, leave_type_filter = "", ""
        if to_date and from_date:
            date_filter = " and modified between DATE('{fd}') and DATE('{td}')".format(fd=from_date, td=to_date)
        if leave_type:
            leave_type_filter = " and name='{lt}'".format(lt=leave_type)

        allocated_leave = {}
        for leave_type in frappe.db.sql(
                '''select name from `tabLeave Type` where (1=1) {ltf}'''.format(ltf=leave_type_filter), as_list=True):
            allocated_leave.setdefault(leave_type[0], [])
            leave = frappe.db.sql(
                "select name, SUM(`total_leaves_allocated`) from `tabLeave Allocation` where employee = '{employee}' and leave_type = '{lt}'"
                " {date_filter} and docstatus = 1".format(employee=employee, lt=leave_type[0], date_filter=date_filter),
                as_list=True)
            allocated_leave[leave_type[0]] = leave
        return allocated_leave

    @classmethod
    def get_seperated_leave(cls, employee, flatten=False, leave_type=None, start_date=None, end_date=None):

        leave_taken = cls.get_approved_leave(employee, leave_type, start_date, end_date)
        leave_allocated = cls.get_allocated_leave(employee, leave_type, start_date, end_date)

        seperated_leave = {}
        for key in leave_taken.keys():
            seperated_leave.setdefault(key, {"taken": 0, "allocated": 0, "balance": 0})
            _taken = leave_taken[key][0][1] or 0
            _allocated = leave_allocated[key][0][1] or 0
            seperated_leave[key] = {key + " - Taken": _taken, key + " - Allocated": _allocated,
                                    key + " - Balance": _allocated - _taken}
        if not flatten:
            return seperated_leave
        else:
            _seperated_leave = {}
            for key, leave in seperated_leave.items():
                _seperated_leave.update(**leave)
            if len(cls.additional_columns) < 1:
                for key in _seperated_leave.keys():
                    cls.additional_columns.append("{key}:Data:150".format(key=key))
            return _seperated_leave
