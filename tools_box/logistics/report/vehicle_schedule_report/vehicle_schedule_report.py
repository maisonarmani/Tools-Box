# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    cconditions = conditions = "(1=1)"

    if filters.get('from') and filters.get('to'):
        conditions += " and date BETWEEN DATE('{from}') and DATE('{to}')"

    if filters.get('vehicle'):
        conditions += " and vehicle = '{vehicle}'"

    if filters.get('type'):
        conditions += " and type = '{type}'"

    if filters.get('ref_name'):
        cconditions += " and ref_name = '{ref_name}'"

    # get all parents
    parents = frappe.db.sql(
        "SELECT name, date, vehicle, type, daily_cost ,'' as ref_name, total_amount amount from `tabVehicle Schedule` "
        "where {0}".format(conditions.format(**filters)), as_dict=1)

    data = []
    for parent in parents:
        parent.update({"parent": None, "indent": 0, "has_value":True})
        data.append(parent)
        children = frappe.db.sql(
            "SELECT ref_name name, '' date, '' vehicle,'' type, 0 daily_cost, ref_name, amount from `tabVehicle Schedule Outbound Item` where {0}"
                .format(cconditions.format(**filters)), as_dict=1)
        for child in children:
            child.update({"parent": parent.name, "indent": 1, "has_value":True})

        data.append(child)

    return get_columns(), data


def get_columns():
    return [{
        "fieldname": "name",
        "label": _("ID"),
        "fieldtype": "Link",
        "options": "Vehicle Schedule",
        "width": 120
    }, {
        "fieldname": "date",
        "label": _("Date"),
        "fieldtype": "Date",
        "options": "",
        "width": 120
    }, {
        "fieldname": "vehicle",
        "label": _("Vehicle"),
        "fieldtype": "Link",
        "options": "",
        "width": 120
    }, {
        "fieldname": "type",
        "label": _("Type"),
        "fieldtype": "Data",
        "options": "",
        "width": 80
    }, {
        "fieldname": "daily_cost",
        "label": _("Daily Cost"),
        "fieldtype": "Data",
        "options": "",
        "width": 120
    }, {
        "fieldname": "ref_name",
        "label": _("Reference Name"),
        "fieldtype": "Link",
        "options": "Delivery Note",
        "width": 120
    }, {
        "fieldname": "amount",
        "label": _("Amount"),
        "fieldtype": "Data",
        "options": "",
        "width": 140
    }]
