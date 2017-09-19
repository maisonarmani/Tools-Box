# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    """ All the report magic happens here """
    return get_column(), get_data(filters)


def get_data(filters):
    conditions = ""
    if filters.get('modified_from') and filters.get('modified_to'):
        conditions += " and tab.modified  BETWEEN '{modified_from}' and '{modified_to}'"
    if filters.get('status'):
        conditions += " and tab.status = '{status}'"

    sql = "select tab.equipment, tab.date, tab.bd_time, tab.status, tab.performed_by, tab.performed_by_name," \
          "tab.type_of_maintenance, tab.start_time,  tab.end_time from `tabEquipment Maintenance Log` tab " \
          "WHERE (1=1) {0}"
    data = frappe.db.sql(sql.format(conditions).format(**filters))
    return data

def get_column():
    return [
        "Equipment:Link/Item:150",
        "Maintenance Date:Date:100",
        "BD Time:Data:120",
        "Status:Data:50",
        "Performed:Link/Employee:100",
        "Performed By Name:Data:150",
        "Type of Maintenance:Data:100",
        "Start Time:Date:150",
        "End Time:Date:150",
    ]
