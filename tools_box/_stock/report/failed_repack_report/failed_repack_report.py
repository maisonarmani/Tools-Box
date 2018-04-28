# Copyright (c) 2015, masonarmani38@gmail.com. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cint, getdate


def execute(filters=None):
    columns = get_columns()
    conditions = ""
    # get all active items and get last valuation rate
    data = frappe.db.sql(
        "SELECT name, posting_date, total_incoming_value , total_outgoing_value , value_difference, company FROM `tabStock Entry` "
        "WHERE purpose='Repack' AND total_incoming_value != total_outgoing_value AND  (1=1) {0}".format(conditions), as_list=1)

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
