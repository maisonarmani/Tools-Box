# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if not filters: filters ={}
	columns = ["Date:Date:100","Doc ID:Link/Expense Claim:150","Expense Claim Type:Link/Expense Claim Type:100","Description:Text:200","Amount:Currency:150","Approver:Link/User:200"]
	conditions = ""
	if filters.get("from_date"):
		conditions += " AND d.expense_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND d.expense_date <= %(to_date)s"
	if filters.get("approver"):
		conditions += " AND p.exp_approver = %(approver)s"
	if filters.get("expense_type"):
		conditions += " AND d.expense_type = %(expense_type)s"
	data = frappe.db.sql("SELECT d.expense_date,p.name,d.expense_type,d.description,d.sanctioned_amount,p.exp_approver FROM `tabExpense Claim` p LEFT JOIN `tabExpense Claim Detail` d ON (p.name = d.parent) WHERE p.docstatus=1 {0}".format(conditions),filters)
	return columns, data
