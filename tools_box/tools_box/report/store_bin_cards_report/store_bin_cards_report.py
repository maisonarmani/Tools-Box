# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt

def execute(filters=None):
	columns, data = ["Store Bin Card No:Link/Store Bin Card:200","Date:Date:200","Item:Link/Item:200","Item Name:Data:200","Opening Qty:Float:200","Receipt Ref No:Data:200","Receipt Qty:Float:100","Issues Ref No:Data:200","Issues Qty:Float:100","Balance Qty:Float:200"], []
	rqty={}
	iqty={}
	item=""
	item2=""
	if filters.get("item"):
		item = " and ii.item_code = '{}'".format(filters.get("item"))
		item2 = " and i.item_code = '{}'".format(filters.get("item"))
	if filters.get("from") and filters.get("from")!="":
		receipt_qty = frappe.db.sql("""select ii.item_code, sum(ii.qty)
			from `tabStore Bin Card Item` ii 
			join `tabStore Bin Card` pp on ii.parent=pp.name 
			where pp.docstatus=1 and pp.date < "{0}" {1} group by ii.item_code """.format(filters.get("from"),item),as_list=1)
		for row in receipt_qty:
			rqty[row[0]]=row[1]
		issued_qty = frappe.db.sql("""select ii.item_code,sum(ii.qty)
			from `tabStore Bin Card Issue Item` ii 
			join `tabStore Bin Card` pp on ii.parent=pp.name 
			where pp.docstatus=1 and pp.date < "{0}" {1} group by ii.item_code """.format(filters.get("from"),item),as_list=1)
		for row in issued_qty:
			iqty[row[0]]=row[1]
	all_data = frappe.db.sql("""select pp.name , pp.date as "date" , ii.item_code,ii.item_name,ii.ref_no,ii.qty,"",""
		from `tabStore Bin Card Item` ii 
		join `tabStore Bin Card` pp on ii.parent=pp.name 
		where pp.docstatus=1 and (pp.date between "{0}" and  "{1}")  {2}
		UNION
		select p.name , p.date as "date" , i.item_code,i.item_name,"","",i.ref_no,i.qty
		from `tabStore Bin Card Issue Item` i 
		join `tabStore Bin Card` p on i.parent=p.name 
		where p.docstatus=1 and (p.date between "{0}" and  "{1}")  {3} 
		order by date""".format(filters.get("from"),filters.get("to"),item,item2),as_list=1)
	#balance = rqty-iqty
	
	for row in all_data:
		r,i,bb,balance=0,0,0,0
		if row[2] in rqty:
			r=flt(rqty[row[2]])
			rqty[row[2]]=flt(rqty[row[2]])+flt(row[5])
		else:
			rqty[row[2]]=flt(row[5])
		if row[2] in iqty:
			i=flt(iqty[row[2]])
			iqty[row[2]]=flt(iqty[row[2]])+flt(row[7])
		else:
			iqty[row[2]]=flt(row[7])
		balance=r-i
		bb=balance
		balance = balance+ flt(row[5])-flt(row[7])
		data.append([row[0],row[1],row[2],row[3],bb,row[4],row[5],row[6],row[7],balance])
		
	return columns, data