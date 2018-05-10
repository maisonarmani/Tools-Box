# Copyright (c) 2015, masonarmani38@gmail.com. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cint, getdate


def execute(filters=None):
    columns = get_columns()
    conditions = ""
    if filters.get('from') and filters.get('to'):
        conditions += " AND se.posting_date BETWEEN DATE('{from}') and DATE('{to}')"

    # get all active items and get last valuation rate
    data = frappe.db.sql(
        "SELECT se.name, se.posting_date, se.total_incoming_value , se.total_outgoing_value , se.value_difference, se.company FROM `tabStock Entry` se "
        "WHERE se.purpose='Repack' AND se.total_incoming_value != se.total_outgoing_value  {0}".format(conditions.format(**filters) ), as_list=1)

    return columns, data


def get_columns():
    """return columns"""
    columns = [
        _("Stock Entry") + ":Link/Stock Entry:150",
        _("Posting Date") + ":Date:100",
        _("Total Incoming Value") + ":Currency:150",
        _("Total Outgoing Value") + ":Currency:150",
        _("Difference Value") + ":Currency:150",
        _("Company") + ":Link/Company:100"
    ]

    return columns
