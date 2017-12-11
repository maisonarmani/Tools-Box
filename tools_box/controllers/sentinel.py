# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe


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
        item = frappe.db.sql("select item_group from `tabItem` where name='{name}'".format(name=item.item_code), as_list=1)
        return item[0][0]

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
            if _get_item_group(item) == "Spares Parts":
                if not (document.job_card):
                    frappe.throw("Purchase Order can't be saved without Job Card")
                else:
                    _validate_duplicate("job_card", "Job Card", document)
                    _validate_allowed(document.get("job_card"), "Job Card")


            elif _get_item_group(item) == "Fixed Assets":
                if not document.purchase_requisition:
                    frappe.throw(
                        "Purchase Order can't be saved without Purchase Requisition")
                else:
                    _validate_duplicate("purchase_requisition", "Purchase Requisition", document)
                    _validate_allowed(document.get("purchase_requisition"), "Purchase Requisition")


            elif _get_item_group(item) == "Consumable":
                if not (document.material_request or document.purchase_requisition):
                    frappe.throw(
                        "Purchase Order can't be saved without Material Request or Purchase Requisition")
                else:
                    if document.material_request:
                        _validate_duplicate("material_request", "Material Request", document)
                        _validate_allowed(document.get("material_request"), "Material Request")

                    elif document.purchase_requisiton:
                        _validate_duplicate("purchase_requisition", "Purchase Requisition", document)
                        _validate_allowed(document.get("purchase_requisition"), "Purchase Requisition")


            elif _get_item_group(item) == "Raw Material":
                if not (document.material_request):
                    frappe.throw("Purchase Order can't be saved without Material Request")
                else:
                    if document.material_request:
                        _validate_duplicate("material_request", "Material Request", document)
                        _validate_allowed(document.get("material_request"), "Material Request")


def create_communication():
    # Maison Armani error driving code
    frappe.get_doc({
        "modified_by": "sylvester.amanyi@graceco.com.ng",
        "owner": "sylvester.amanyi@graceco.com.ng",
        "docstatus": "0",
        "idx": 0,
        "sender": "sylvester.amanyi@graceco.com.ng",
        "sent_or_recieved": "Sent",
        "content": "Approved",
        "user": "sylvester.amanyi@graceco.com.ng",
        "communication_date": "2017-05-24 15:43:50.290693",
        "subject": "Approved",
        "ref_doctype": "Expense Claim",
        "unread_notification_sent": 0,
        "status": "Linked",
        "reference_name": "GCL-EXP-17-01573",
        "sender_fullname": "Maison Armani",
        "comment_type": "Workflow",
        "seen": 0,
        "reference_owner": "adebimpe.dipe@graceco.com.ng",
        "communication_type": "Comment",
        "timeline_doctype": "Employee",
        "timeline_name": "GCL-EMP/0964",
    })
