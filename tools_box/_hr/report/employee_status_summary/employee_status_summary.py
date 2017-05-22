# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe


def execute(filters=None):
    columns, data = get_columns(filters), get_data(filters)
    return columns, data

def get_data(filters=None):
    conditions, data = "SELECT employee, employee_name, employment_type, date_of_joining, status ,relieving_date FROM `tabEmployee` WHERE (1=1)", []
    date_type = "date_of_joining"

    if filters.get("status") == "Left" : date_type = "relieving_date"
    if filters.get("from_date"):
        conditions += " AND {dt} >= '%(from_date)s'".format(dt=date_type)
    if filters.get("to_date"):
        conditions += " AND {dt} <= '%(to_date)s'".format(dt=date_type)
    if filters.get("status") and filters.get("status")  != "All":
        conditions += " AND status = '%(status)s'"
    if filters.get("employment_type") and filters.get("employment_type") != 'All':
        conditions += " AND employment_type = '%(employment_type)s'"

    frappe.errprint(conditions % filters)

    misc = " ORDER BY employee_name,status ASC"
    if conditions:
        data = frappe.db.sql(conditions % filters + misc)
    return data


def get_columns(filters):
    column = [
        _("Employee ID") + ":Link/Employee:120",
        _("Name") + ":Data:200",
        _("Employment Type") + ":Data:150",
        _("Joined Date") + ":Date:130",
        _("Status") + ":Data:70",
    ]

    if filters.get('status') == "Left":
        column.append(_("Relieving Date") + ":Date:130")
    return column