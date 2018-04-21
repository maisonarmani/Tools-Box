# -*- coding: utf-8 -*-
# Copyright (c) 2018, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EquipmentSupport(Document):
	pass



@frappe.whitelist()
def close_ticket(ticket_no):
    # check to see if the hdt has a job card
    # check if the jobcard has been completed
    comp_work_order = frappe.db.sql(
        "SELECT status FROM `tabWork Order` WHERE ticket_number = '{0}'".format(ticket_no))

    if comp_work_order and comp_work_order[0].status != "Completed":
        frappe.throw("Sorry, you can't close this ticket as the work order attached has not been completed.")
    else:
        frappe.db.sql("Update `tabEquipment Support`  set status='Closed', docstatus = 1 where name = '{0}'".format(ticket_no))

