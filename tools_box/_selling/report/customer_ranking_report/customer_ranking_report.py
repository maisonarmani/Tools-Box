# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from datetime import date, datetime

import frappe
from frappe import _


def execute(filters=None):
    # get all customers and last invoice date
    if filters.get('to') and filters.get('from'):
        customers = frappe.db.sql(
            "SELECT DISTINCT customer, name invoice ,territory, posting_date lpd FROM `tabSales Invoice` "
            "WHERE docstatus = 1 ORDER BY posting_date DESC ", as_dict=1)

        columns, data = get_cols(), []

        _to, _from = datetime.strptime(filters.get('to'), '%Y-%m-%d'), datetime.strptime(filters.get('from'),
                                                                                         '%Y-%m-%d')
        diff = (_to - _from).days
        class_diff = diff / 5.0

        ranges = []
        _customers = []
        for n in range(1, 6):
            ranges.append(class_diff * n)

        for cust in customers:
            if cust.customer not in _customers:
                _customers.append(cust.customer)
            else:
                continue
            lpd = datetime.strptime(str(cust.get('lpd')), '%Y-%m-%d')
            cust_diff = (lpd - _from).days
            if cust_diff <= ranges[0]:
                cust.update({"rank": 1})
                data.append(cust)

            elif cust_diff > ranges[0] and cust_diff <= ranges[1]:
                cust.update({"rank": 2})
                data.append(cust)

            elif cust_diff > ranges[1] and cust_diff <= ranges[2]:
                cust.update({"rank": 3})
                data.append(cust)

            elif cust_diff > ranges[2] and cust_diff <= ranges[3]:
                cust.update({"rank": 4})
                data.append(cust)

            elif cust_diff > ranges[3] and cust_diff <= ranges[4]:
                cust.update({"rank": 5})
                data.append(cust)

        del _customers
        return columns, data


def get_cols():
    return [{
        "fieldname": "invoice",
        "label": _("Reference Document"),
        "fieldtype": "Link",
        "options": "Sales Invoice",
        "width": 150
    }, {
        "fieldname": "customer",
        "label": _("Customer Name"),
        "fieldtype": "Data",
        "width": 160
    }, {
        "fieldname": "territory",
        "label": _("Territory"),
        "fieldtype": "Link",
        "options": "Territory",
        "width": 120
    }, {
        "fieldname": "lpd",
        "label": _("Last Purchase Date"),
        "fieldtype": "Date",
        "width": 120
    }, {
        "fieldname": "rank",
        "label": "Rank",
        "fieldtype": "Int",
        "width": 40
    }]
