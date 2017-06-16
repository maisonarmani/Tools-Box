# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    """ All the report magic happens here """
    return get_column(), get_column(filters)


def get_data(filters):
    conditions = ""
    if filters.get('modified_from') and filters.get('modified_to'):
        conditions += " and tab._date  BETWEEN '{0}' and '{1}'"\
            .format(filters.get("modified_from"),filters.get('modified_to'))

    sql = "select * from `tabEquipment Maintenance Log` WHERE {0}"

    # frappe.errprint(sql.format(conditions))
    data = frappe.db.sql(sql.format(conditions))

def get_column():
    # ["Link:Link/Accident:150", "Data:Data:200", "Currency:Currency:100", "Float:Float:100"]
    return [
        "Link:Link/Accident:150",
        "Data:Data:200",
        "Currency:Currency:100",
        "Float:Float:100"
    ]
