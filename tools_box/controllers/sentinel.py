# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe


def validate_states(document,trigger):
    frappe.errprint(document)
    frappe.errprint(trigger)