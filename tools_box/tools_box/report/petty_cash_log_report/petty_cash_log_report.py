# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt

def execute(filters=None):
	columns, data = ["Petty Cash Log:Link/Petty Cash Log:200","Date:Date:200","Type::100","Reference:Data:200","Referece No:Dynamic Link/Reference:200","Opening:Currency:200","Receipt:Currency:200","Payment:Currency:200","Balance:Currency:200"], []
	rqty=0
	pqty=0
	all_data=[]
	if filters.get("type")=="Payment":
		all_data = frappe.db.sql("""select pp.name , pp.date as "date" ,pp.transaction_type,ii.ref_doc,ii.ref_no,ii.currency,""
			from `tabPetty Cash Log Item Sales` ii 
			join `tabPetty Cash Log` pp on ii.parent=pp.name 
			where pp.docstatus=1 and (pp.date between "{0}" and  "{1}")  
			order by date""".format(filters.get("from"),filters.get("to")),as_list=1)
	elif filters.get("type")=="Receipt":
		all_data = frappe.db.sql("""select p.name , p.date as "date" ,p.transaction_type,i.ref_doc,i.ref_no,"",i.currency
			from `tabPetty Cash Log Item` i 
			join `tabPetty Cash Log` p on i.parent=p.name 
			where p.docstatus=1 and (p.date between "{0}" and  "{1}") 
			order by date""".format(filters.get("from"),filters.get("to")),as_list=1)
	else:
		receipt_qty = frappe.db.sql("""select sum(ii.currency)
			from `tabPetty Cash Log Item Sales` ii 
			join `tabPetty Cash Log` pp on ii.parent=pp.name 
			where pp.docstatus=1 and pp.date < "{0}" group by pp.transaction_type """.format(filters.get("from")),as_list=1)
		for row in receipt_qty:
			rqty+=row[0]
		payment_qty = frappe.db.sql("""select sum(ii.currency)
			from `tabPetty Cash Log Item` ii 
			join `tabPetty Cash Log` pp on ii.parent=pp.name 
			where pp.docstatus=1 and pp.date < "{0}" group by pp.transaction_type """.format(filters.get("from")),as_list=1)
		for row in payment_qty:
			pqty+=row[0]
		all_data = frappe.db.sql("""select pp.name , pp.date as "date" ,pp.transaction_type,ii.ref_doc,ii.ref_no,ii.currency,""
			from `tabPetty Cash Log Item Sales` ii 
			join `tabPetty Cash Log` pp on ii.parent=pp.name 
			where pp.docstatus=1 and (pp.date between "{0}" and  "{1}")  
			UNION
			select p.name , p.date as "date" ,p.transaction_type,i.ref_doc,i.ref_no,"",i.currency
			from `tabPetty Cash Log Item` i 
			join `tabPetty Cash Log` p on i.parent=p.name 
			where p.docstatus=1 and (p.date between "{0}" and  "{1}") 
			order by date""".format(filters.get("from"),filters.get("to")),as_list=1)
	balance = rqty-pqty
	for row in all_data:
		bb=balance
		balance = balance+ flt(row[5])-flt(row[6])
		data.append([row[0],row[1],row[2],row[3],row[4],bb,row[5],row[6],balance])
	return columns, data
