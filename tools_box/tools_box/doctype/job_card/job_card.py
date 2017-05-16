# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
class JobCard(Document):
	def validate(self):
		if not self.requested_by:
			if self.ticket_number:
	                        self.requested_by = get_requested_by(self.ticket_number)
		
		if not self.employee_name:
			if self.ticket_number:	
				self.employee_name = get_employee_name(self.employee_name)

		subtotal = 0
		for item in self.job_card_material_detail:
			if not item.item_name:
				item.item_name = get_item_name(item.item_code)
			subtotal = subtotal + item.total
		self.materials_total = subtotal
		self.job_card_total = self.materials_total + self.labour_fees + self.transport_fare
		self.balance_due_upon_job_completion = self.job_card_total - self.job_advance

		#if self.job_completion_date:
		#	if not 'Helpdesk Admin' in frappe.get_roles():
		#		frappe.throw('Only Helpdesk Admin can complete the Job Card.')
		#	else:
		#		self.status = 'Completed'

		#if self.status == 'Completed':
		#	if not self.job_completion_date:
		#		frappe.throw('Job completion date is not set.')

@frappe.whitelist()
def get_requested_by(ticket_number):
	ticket = frappe.get_doc("Helpdesk Ticket", ticket_number)
	employee = frappe.get_doc("Employee", ticket.raised_by)

	return employee.name

@frappe.whitelist()
def get_employee_name(ticket_number):
	ticket = frappe.get_doc("Helpdesk Ticket", ticket_number)
	employee = frappe.get_doc("Employee",ticket.raised_by)

	return employee.employee_name

@frappe.whitelist()
def get_item_name(item_code):
	item = frappe.get_doc("Item",item_code)
	
	return item.item_name

@frappe.whitelist()
def get_item_description(item_code):
	item = frappe.get_doc("Item",item_code)
	return item.description

@frappe.whitelist()
def get_job_cards(start, end):
	data = frappe.db.sql("""select name, job_card_date, proposed_completion_date, job_description, status from `tabJob Card` where ((ifnull(job_card_date, '0000-00-00')!= '0000-00-00') and (job_card_date between %(start)s and %(end)s) or ((ifnull(job_card_date, '0000-00-00')!= '0000-00-00') and proposed_completion_date between %(start)s and %(end)s))""", { "start": start, "end": end }, as_dict=True)
	return data
@frappe.whitelist()
def make_purchase_order(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.ignore_pricing_rule = 1
		target.run_method("set_missing_values")
		target.run_method("get_schedule_dates")
		target.run_method("calculate_taxes_and_totals")

	target_doc = get_mapped_doc("Job Card", source_name, {
		"Job Card": {
			"doctype": "Purchase Order",
			"field_map":{
				"vendor":"supplier",
				"job_card_date":"transaction_date",
				"name":"job_card"
			}
		},
		"Job Card Material Detail": {
			"doctype": "Purchase Order Item",
			"field_map": {
				"item_code": "item_code",
				"item_name": "item_name",
				"item_description": "description",
				"uom":"stock_uom",
				"no_of_units":"qty",
				"unit_cost":"rate",
				"conversion_factor":1,
				"total":"amount"
			}
		}
	}, target_doc,set_missing_values)

	return target_doc
