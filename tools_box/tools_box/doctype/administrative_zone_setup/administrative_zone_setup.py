# -*- coding: utf-8 -*-
# Copyright (c) 2018, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class AdministrativeZoneSetup(Document):
    pass


def get_permission_query_conditions_for_s(user, doctype):
    _user = frappe.get_doc("User", user)

    # frappe.errprint(doctype)
    # ad_zone = frappe.get_("Administrative Zone")
    if "System Manager" in frappe.get_roles(user) or _user.administrative_zone == None:
        return None
    else:
        # frappe.errprint(_user.administrative_zone)
        return """(`tab{doctype}`.owner = '{user}') or (`tab{doctype}`.administrative_zone= '{ad_zone}')""".format(
            user=frappe.db.escape(user), ad_zone=_user.administrative_zone, doctype=doctype)


@frappe.whitelist(False)
def get_administrative_zone():
    return dict(
        administrative_zone = frappe.get_doc("User", frappe.session.user).administrative_zone
    )



@frappe.whitelist(False)
def get_administrative_defaults(administrative_zone):
    return frappe.db.sql(
        "SELECT default_warehouse, default_territory FROM `tabAdministrative Zone Setup Item` WHERE administrative_zone='%s'" % administrative_zone,
        as_dict=1)


def get_permission_query_conditions_for_sales_invoice(user):
    return get_permission_query_conditions_for_s(user, "Sales Invoice")


def get_permission_query_conditions_for_atl(user):
    return get_permission_query_conditions_for_s(user, "Authority to Load")


def get_permission_query_conditions_for_customer(user):
    return get_permission_query_conditions_for_s(user, "Customer")


def get_permission_query_conditions_for_del_note(user):
    return get_permission_query_conditions_for_s(user, "Delivery Note")


def get_permission_query_conditions_for_sales_order(user):
    return get_permission_query_conditions_for_s(user, "Sales Order")
