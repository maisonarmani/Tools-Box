# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class HelpdeskTicket(Document):
    def validate(self):
        ticket_number = self.name
        attached_job_cards = frappe.db.sql(
            "SELECT status FROM `tabJob Card` WHERE ticket_number = '{0}'".format(ticket_number))

        if len(attached_job_cards):
            if not 'Helpdesk Admin' in frappe.get_roles():
                frappe.throw('Only Helpdesk Admin can edit a ticket that has job cards')

        # if self.assigned_to:
        #	if not 'Helpdesk Admin' in frappe.get_roles():
        #		frappe.throw('Only Helpdesk Admin can assign tickets.')

        if not self.raised_by_name:
            if self.raised_by:
                self.raised_by_name = get_full_name(self.raised_by)

        if self.status == 'Draft':
            self.status = 'Open'

        # if self.assigned_to and self.status != 'On-Hold' and self.status !='Close':
        #	if not 'Helpdesk Admin' in frappe.get_roles():
        #		frappe.throw('Only Helpdesk Admin can assign tickets.')
        #	else:
        #		self.status = 'Assigned'

        if self.status == 'On-Hold':
            if not 'Helpdesk Admin' in frappe.get_roles():
                frappe.throw('Only Helpdesk Admin can change the status to On-Hold.')

        if self.status == 'Close':
            if frappe.get_user() is not self.created_by:
                frappe.throw('Only the creator can close the ticket.')
            for attached_job_card in attached_job_cards:
                if attached_job_card[0] != 'Completed':
                    frappe.throw('Cannot save while attached Job Card is not complete.')

        if self.status == 'Assigned':
            if not self.assigned_to:
                frappe.throw('The assigned to field is empty.')


@frappe.whitelist()
def close_ticket(ticket_no):
    # check to see if the hdt has a job card
    # check if the jobcard has been completed
    comp_job_cards = frappe.db.sql(
        "SELECT status FROM `tabJob Card` WHERE ticket_number = '{0}'".format(ticket_no))

    if comp_job_cards and comp_job_cards[0].status != "Completed":
        frappe.throw("Sorry, you can't close this ticket as the job card attached has not been completed.")
    else:
        frappe.db.sql("Update `tabHelpdesk Ticket`  set status='Close', docstatus = 1 where name = '{0}'".format(ticket_no))


@frappe.whitelist()
def get_full_name(raised_by):
    employee = frappe.get_doc("Employee", raised_by)

    # concatenates by space if it has value
    return employee.employee_name
