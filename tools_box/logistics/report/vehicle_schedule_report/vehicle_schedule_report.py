# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    return get_columns(filters.type), get_data(filters)


def get_data(filters):
    conditions = ""

    if filters.get('from') and filters.get('to'):
        conditions += " and date BETWEEN DATE('{from}') and DATE('{to}')"

    if filters.get('vehicle'):
        conditions += " and p.vehicle = '{vehicle}'"

    if filters.get('type'):
        conditions += " and p.type = '{type}'"

    if filters.get('ref_name'):
        conditions += " and c.ref_name = '{ref_name}'"

    if filters.get('type') != "Operations":
        data = frappe.db.sql("""select p.date, p.name, p.vehicle, p.type,p.daily_cost, p.total_amount, p.remark 
        from `tabVehicle Schedule` as p JOIN `tabVehicle Schedule {type} Item` c 
        WHERE (1=1) {c} GROUP BY name""".format(c=conditions.format(**filters), type=filters.get('type')), as_list=1)

        for d in data:
            _ = round(((d[4] / d[5]) * 100), 2)
            d.append(_)

        return data
    else:
        data = frappe.db.sql("""select p.date, p.name, p.vehicle, p.type,p.daily_cost, p.description, p.total_amount 
                from `tabVehicle Schedule` as p WHERE (1=1) {c}""".format(c=conditions.format(**filters)), as_list=1)
        frappe.errprint(data)
        return data


def get_columns(stype):
    if stype != "Operations":
        return [
            "Date:Date:100",
            "ID:Link/Vehicle Schedule:100",
            "Vehicle:Link/Vehicle:100",
            "Type:Data:100",
            "Daily Cost:Currency:100",
            "Amount:Currency:130",
            "Remark:Data:260",
            "Ratio:Float:120"
        ]
    else:
        return [
            "Date:Date:100",
            "ID:Link/Vehicle Schedule:100",
            "Vehicle:Link/Vehicle:100",
            "Type:Data:100",
            "Daily Cost:Currency:100",
            "Description:Data:200",
            "Amount:Currency:130"
        ]
