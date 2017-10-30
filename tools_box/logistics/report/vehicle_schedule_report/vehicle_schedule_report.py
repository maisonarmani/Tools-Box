# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    data, conditions = [], ""
    columns = [
        "Date:Date:100",
        "Vehicle:Link/Vehicle:100",
        "Type:Data:100",
        "Remark:Data:260",
        "Ref Type:Data:120",
        "Ref Name:Data:130",
        "Status:Data:130",
        "Amount:Currency:130"
    ]

    if filters.get('from') and filters.get('to'):
        conditions += " and date BETWEEN DATE('{from}') and DATE('{to}')"

    if filters.get('vehicle'):
        conditions += " and p.vehicle = '{vehicle}'"

    if filters.get('type'):
        conditions += " and p.type = '{type}'"

    schedules = frappe.db.sql("""select name from `tabVehicle Schedule` p where (1=1) {cond} """
                              .format(cond=conditions.format(**filters)), as_dict=1)

    for schedule in schedules:
        data.extend(list(__get_bound(schedule.name, filters.get('type'), filters.get('status')))[0:])

    return columns, data


def __get_bound(name=None, type=None, status=None):
    if status:
        status = " and c.status = '{0}'".format(status)
    if name:
        name = " and p.name = '{0}'".format(name)
    items = frappe.db.sql("""select p.date, p.vehicle, p.type, p.remark, c.ref_type, c.ref_name,
	 c.status, c.amount from `tabVehicle Schedule` as p JOIN `tabVehicle Schedule {type} Item` as c ON(c.parent = p.name) WHERE (1=1) {name} {status}"""
                          .format(name=name, type=type, status=status))
    return items
