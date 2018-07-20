# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe


def check_clean(document, trigger):
    return True
    _ = frappe.db.sql("""select name from `tabProduction Order` where production_item = '{item}' 
                      and status not in ("Completed", "Resolved","Cancelled","Stopped") and docstatus = 1 and name != '{name}' """
                      .format(item=document.production_item, name=document.name), as_list=1)
    if len(_):
        frappe.throw("""Sorry, new production order for {1} cannot be created, since we have a different production order {0} that
                     has not been completed or resolved""".format(_[0][0], document.production_item))


def validate_required(document, trigger):
    def _validate_duplicate(field, doctype, document):
        if document.get(field):
            _ = frappe.db.sql("""select name from `tabPurchase Order` where name != '{name}' and workflow_state="Approved" 
                            and {field}="{obj}" """.format(field=field, name=document.name, obj=document.get(field)),
                              as_list=1)

            if bool(len(_)):
                frappe.throw("{dt} already attached to approved Purchase Order {po}"
                             .format(dt=doctype, po=_[0][0]))

    def _validate_allowed(name, doctype):
        state = "status"
        if doctype == "Job Card":
            state = "workflow_state"
        if name:
            _ = frappe.db.sql(
                """select name from `tab{dt}` where name = '{name}' and docstatus = 1 or {state} 
                      in ("Approved", "Authorized","Awaiting Purchase Order") """
                    .format(name=name, dt=doctype, state=state), as_list=1)

            if not bool(len(_)):
                frappe.throw("{dt} attached has not been approved".format(dt=doctype))

    def _get_item_group(item):
        item = frappe.db.sql("select item_group from `tabItem` where name='{name}'".format(name=item.item_code),
                             as_list=1)
        return item[0][0]

    def _is_fueling(item):
        item = frappe.db.sql("select name from `tabItem` where name='{name}' and (item_name LIKE 'Fueling%' or "
                             "item_name LIKE 'Fuelling%')".format(name=item.item_code), as_list=1)
        return item != []

    def _is_new(name):
        _ = frappe.db.sql("select name from `tabPurchase Order` where name='{name}'".format(name=name),
                          as_list=1)
        return _ == []

    if _is_new(document.name):
        for item in document.items:
            # Raw material need material request
            # Spare parts needs job card
            # Consumable needs Purchase req or material request
            # Fixed Assets needs purchase requisition

            item_grp = _get_item_group(item)
            if item_grp in ("Spares Parts", "Spare Parts"):
                if not document.job_card and not document.purchase_requisition and not document.material_request:
                    frappe.throw(
                        "Purchase Order can't be saved without Job Card,Purchase Requisition or Material Request")
                else:
                    _validate_duplicate("job_card", "Job Card", document)
                    _validate_allowed(document.get("job_card"), "Job Card")

            elif item_grp == "Fixed Assets":
                if not document.purchase_requisition:
                    frappe.throw(
                        "Purchase Order can't be saved without Purchase Requisition")
                else:
                    _validate_duplicate("purchase_requisition", "Purchase Requisition", document)
                    _validate_allowed(document.get("purchase_requisition"), "Purchase Requisition")

            elif item_grp in ("Consumable", "QC Lab") and not _is_fueling(item):
                if not (document.material_request or document.purchase_requisition):
                    frappe.throw(
                        "Purchase Order can't be saved without Material Request or Purchase Requisition")
                else:
                    if document.material_request:
                        # _validate_duplicate("material_request", "Material Request", document)
                        _validate_allowed(document.get("material_request"), "Material Request")

                    elif document.purchase_requisition:
                        _validate_duplicate("purchase_requisition", "Purchase Requisition", document)
                        _validate_allowed(document.get("purchase_requisition"), "Purchase Requisition")

            elif item_grp in ("Raw Material", "QC Lab"):
                if not (document.material_request):
                    frappe.throw("Purchase Order can't be saved without Material Request")
                else:
                    if document.material_request:
                        # _validate_duplicate("material_request", "Material Request", document)
                        _validate_allowed(document.get("material_request"), "Material Request")
