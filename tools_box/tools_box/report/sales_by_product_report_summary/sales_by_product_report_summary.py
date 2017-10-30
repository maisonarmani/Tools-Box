# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Item:Link/Item:200","Item Name:Data:200","Qty:Float:200","Amount:Currency:150", "Discount:Currency:100"], []

	conds = "(si.posting_date between '{from}' and '{to}')"
	if filters.get("item"):
		conds += """ and soi.item_code = '{item}' """
	if filters.get("customer"):
		conds += """ and si.customer = '{customer}' """
	if filters.get("territory"):
		conds += """ and si.territory = '{territory}' """


	# get all the children account in the sales income
	sub_accs = frappe.db.sql("select name from `tabAccount` where parent_account='Sales Income - GCL'", as_list=1)

	s_accs = ()
	for sub_acc in sub_accs:
		s_accs += (str(sub_acc[0]),)

	data = frappe.db.sql("""SELECT soi.item_code,soi.item_name,sum(soi.qty),sum(soi.net_amount) as net_amount, 
				IFNULL(SUM(si.discount_amount),0) as discount_amount  FROM `tabSales Invoice Item` soi JOIN `tabSales Invoice` si
				ON(soi.parent=si.name) where si.docstatus=1 AND soi.income_account IN {s_accs}  AND {conds} GROUP BY soi.item_code"""
						 .format(s_accs = str(s_accs), conds = conds.format(**filters)), as_list=1)
	return columns, data


