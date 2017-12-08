# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe


def validate_required(document, trigger):
    return True
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
                """select name from `tab{dt}` where name = '{name}' and docstatus = 1 or {state} in ("Approved", "Authorized","Awaiting Purchase Order") """
                    .format(name=name, dt=doctype, state=state), as_list=1)

            if not bool(len(_)):
                frappe.throw("{dt} attached has not been approved"
                             .format(dt=doctype))

    def _is_raw_material(item):
        item = frappe.db.sql("select name from `tabItem` where name='{name}' and item_group='Raw Material' "
                             .format(name=item),
                             as_list=1)
        return item != []

    def _is_new(name):
        _ = frappe.db.sql("select name from `tabPurchase Order` where name='{name}'".format(name=name),
                             as_list=1)
        return _ == []

    if _is_new(document.name):
        for item in document.items:
            # if _is_raw_material(item.item_code):
            # pass
            # purchase requisition or job card is required
            if not (document.purchase_requisition or document.vehicle_schedule
                    or document.material_request or document.job_card):
                frappe.throw("Purchase Order {name} can't be saved without Purchase Requisition, "
                             "Vehicle Schedule, Material Request or Job Card".format(name=document.name))
            else:
                # check that purchase_req, veh_sch, job_card doesn't exist on an approved po
                _validate_duplicate("purchase_requisition", "Purchase Requisition", document)
                _validate_duplicate("job_card", "Job Card", document)
                _validate_duplicate("vehicle_schedule", "Vehicle Schedule", document)
                #_validate_duplicate("material_request", "Material Request", document)

                _validate_allowed(document.get("purchase_requisition"), "Purchase Requisition")
                _validate_allowed(document.get("job_card"), "Job Card")
                _validate_allowed(document.get("vehicle_schedule"), "Vehicle Schedule")
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
