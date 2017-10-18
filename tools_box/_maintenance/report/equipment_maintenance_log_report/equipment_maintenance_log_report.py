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
    if filters.get('type_of_maintenance'):
        conditions += " and tab.type_of_maintenance = '{m_type}'"
    if filters.get('equipment'):
        conditions += " and tab.equipment = '{equipment'}"

    sql = "select tab.equipment, tab.date, tab.status, tab.performed_by, tab.performed_by_name," \
          "tab.type_of_maintenance, tab.start_time,  tab.end_time, tab.bd_time from `tabEquipment Maintenance Log` tab " \
          "WHERE (1=1) {0}"
    data = frappe.db.sql(sql.format(conditions).format(**filters))
    return data

def get_column():
    return [
        "Equipment:Link/Asset:150",
        "Maintenance Date:Date:150",
        "Status:Data:100",
        "Performed:Link/Employee:100",
        "Performed By Name:Data:150",
        "Type of Maintenance:Data:150",
        "Start Time:Date:120",
        "End Time:Date:120",
        "BD Time:Data:120",

    ]
