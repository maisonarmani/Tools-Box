# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from tools_box.controllers.api import get_approver_authorizer
from frappe.model.document import Document


class EquipmentMaintenanceLog(Document):
    pass


@frappe.whitelist()
def make_job_card(docname):
    import datetime

    def validate():
        g = frappe.db.sql("""select name from `tabJob Card` where equipment_maintenance_log=%s""", eqml.name)
        return g[0][0] if g else ""

    def _get_item(asset):
        g = frappe.db.sql("""select tabAsset.item_code, tabItem.item_name,tabItem.item_code,tabItem.description, tabItem.stock_uom 
            from `tabAsset` INNER JOIN tabItem ON(tabItem.item_code =  tabAsset.item_code) where tabAsset.name = '%s'""" % asset,
                          as_dict=1)
        return g[0]

    eqml = frappe.get_doc("Equipment Maintenance Log", docname)
    g = validate()
    if g:
        frappe.throw(_("Job Card {0} already exists for the Equipment Maintenance Log").format(g))


    g = frappe.new_doc("Job Card")
    g.date = datetime.datetime.today()
    g.equipment_maintenance_log = eqml.name
    g.company = "Graceco Limited"
    g.asset_category = eqml.category
    g.approver = get_approver_authorizer(eqml.performed_by)[0].get('approver_user_id')
    g.asset = eqml.equipment
    g.proposed_completion_date  = eqml.end_time
    g.job_description  = eqml.m_description
    g.job_card_date  = datetime.datetime.today()
    g.employee_name  = eqml.performed_by

    g.priority = "Medium"
    g.materials_total = eqml.service_fee
    g.labour_fees = eqml.labour_fee
    g.job_card_total= eqml.total

    item = _get_item(eqml.equipment)
    g.append("job_card_material_detail", {
        "item_code": item.item_code,
        "item_name": item.item_name,
        "uom": item.stock_uom,
        "item_description": item.description,
        "no_of_units": 1,
        "unit_cost":eqml.total,
        "total":eqml.total
    })

    return g.as_dict()



