# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

def validate_status(document,trigger):
    print "validate status"
    sanitized = ["Sales Order","Purchase Order","Expense Claim"]
    for doc in sanitized:
        # clean the error
        frappe.db.sql("update `tab{}` set workflow_state = \"Draft\" where workflow_state = 'Approved' and docstatus = 0 "
                      .format(doc))
        # mark all closed as closed
        frappe.db.sql("update `tab{}` set workflow_state = \"Closed\" where workflow_state = 'Approved' and status = "
                      "'Closed' ".format(doc))

def create_communication():
    # Maison Armani error driving code
    frappe.get_doc({
        "modified_by":"sylvester.amanyi@graceco.com.ng",
        "owner":"sylvester.amanyi@graceco.com.ng",
        "docstatus":"0",
        "idx":0,
        "sender":"sylvester.amanyi@graceco.com.ng",
        "sent_or_recieved":"Sent",
        "content":"Approved",
        "user":"sylvester.amanyi@graceco.com.ng",
        "communication_date":"2017-05-24 15:43:50.290693",
        "subject":"Approved",
        "ref_doctype":"Expense Claim",
        "unread_notification_sent":0,
        "status":"Linked",
        "reference_name":"GCL-EXP-17-01573",
        "sender_fullname":"Maison Armani",
        "comment_type":"Workflow",
        "seen":0,
        "reference_owner":"adebimpe.dipe@graceco.com.ng",
        "communication_type":"Comment",
        "timeline_doctype":"Employee",
        "timeline_name":"GCL-EMP/0964",
    })