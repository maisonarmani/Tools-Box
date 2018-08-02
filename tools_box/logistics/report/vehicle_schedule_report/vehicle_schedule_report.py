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
        "SELECT name, '' customer, date,vehicle, type, daily_cost ,'' ref_name, total_amount amount  from `tabVehicle Schedule` "
        "where {0}".format(conditions.format(**filters)), as_dict=1)
    data = []
    for index, parent in enumerate(parents):
        rat = (parent.daily_cost / parent.amount) * 100
        parent.update({"parent": None, "indent": 0, "has_value": True, "ratio": rat})
        data.append(parent)

        if filters.get('type') != "Operations":
            children = frappe.db.sql(
                "SELECT name, ref_name , party, amount from `tabVehicle Schedule {2} Item` where {0} and parent = '{1}' "
                    .format(cconditions.format(**filters), parent.name, filters.get('type')), as_dict=1)

            for child in children:
                data.append(
                    dict(name="", customer=child.get('party'), date="", vehicle="",
                         type="", daily_cost="", ref_name=child.get('ref_name'),
                         indent=1, amount=child.get('amount'), ratio=0,
                         parent=parent.get('name'), has_value=True)
                )

    doc = "Delivery Note"
    if filters.get('type') == "Inbound":
        doc = "Purchase Order"

    return get_columns(doc), data


def get_columns(doc):
    return [{
        "fieldname": "name",
        "label": _("ID"),
        "fieldtype": "Link",
        "options": "Vehicle Schedule",
        "width": 160
    }, {
        "fieldname": "customer",
        "label": _("Customer"),
        "fieldtype": "data",
        "width": 160
    }, {
        "fieldname": "date",
        "label": _("Date"),
        "fieldtype": "Date",
        "width": 120
    }, {
        "fieldname": "vehicle",
        "label": _("Vehicle"),
        "fieldtype": "Link",
        "options": "Vehicle",
        "width": 120
    }, {
        "fieldname": "type",
        "label": _("Type"),
        "fieldtype": "Data",
        "options": "data",
        "width": 80
    }, {
        "fieldname": "daily_cost",
        "label": _("Daily Cost"),
        "fieldtype": "Currency",
        "options": "currency",
        "width": 120
    }, {
        "fieldname": "ref_name",
        "label": _(doc),
        "fieldtype": "Link",
        "options": doc,
        "width": 120
    }, {
        "fieldname": "amount",
        "label": _("Amount"),
        "fieldtype": "Currency",
        "options": "currency",
        "width": 140
    }, {
        "fieldname": "ratio",
        "label": _("Ratio"),
        "fieldtype": "Float",
        "options": "",
        "width": 100
    }]
