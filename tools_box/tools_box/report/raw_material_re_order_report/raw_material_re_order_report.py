# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Item Code:Link/Item:200","Item Name::200","Current Level:Float:100","Re-order Level:Float:100","Re-order Qty:Float:100","Lead Time:Int:100"], []
	#Item code	Item Name	Current Level	Re-order level	Re-order Qty	Lead time
	#					<from stock ledger>	<from item>		<from item>	<from item>
	data = frappe.db.sql("""select s.item_code,it.item_name, s.qty_after_transaction,i.warehouse_reorder_level,i.warehouse_reorder_qty,it.lead_time_days
		from `tabStock Ledger Entry` s 
		join (
			select ss.item_code,max(addtime(ss.posting_date,ss.posting_time)) as "latest"
			from `tabStock Ledger Entry` ss where ss.warehouse="{0}" group by ss.item_code  
			) sd on s.item_code=sd.item_code and addtime(s.posting_date,s.posting_time)=sd.latest
		join `tabItem Reorder` i on i.parent=s.item_code and i.warehouse = "{0}"
		join `tabItem` it on it.item_code=s.item_code
		where s.qty_after_transaction < i.warehouse_reorder_level
		""".format(filters.get("warehouse")), as_list=1)
	items = frappe.db.sql("""select i.parent,it.item_name,"0",i.warehouse_reorder_level,i.warehouse_reorder_qty,it.lead_time_days 
		from `tabItem Reorder` i 
		join `tabItem` it on it.item_code=i.parent
		where i.warehouse = "{0}" and i.parent NOT IN (select s.item_code from `tabStock Ledger Entry` s group by s.item_code)""".format(filters.get("warehouse")), as_list=1)
	for x in items:
		data.append(x)
	return columns, data


