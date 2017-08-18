# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    """ All the report magic happens here """
    columns, data = get_column(), []
    conditions = "(1=1) "

    if filters.get('fire_extinguisher'):
        conditions += ' and tabFA.fire_extinguisher_used = \'{0}\''.format(filters.get('fire_extinguisher'))
    if filters.get('reported_by'):
        conditions += ' and tabFA.reported_by = \'{0}\''.format(filters.get('reported_by'))

    sql = '''select FA.name accident, FA.nature_of_accident,FA.fire_extinguisher_used, 
            FA.location , FA.reported_by, FA.reported_on from `tabFire Accident Form` FA WHERE {0}'''

    # frappe.errprint(sql.format(conditions))
    data = frappe.db.sql(sql.format(conditions))
    return columns, data


def get_column():
    return [
        "Name:Data:200",
        "Nature of Accident:Data:200",
        "Fire Extinguisher Used:Link/Fire Extinguisher:150",
        "Location: Data:150",
        "Reported By:Data:100",
        "Reported On:Date:100"
    ]
