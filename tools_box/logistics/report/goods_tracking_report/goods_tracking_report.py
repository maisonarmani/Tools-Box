# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if not filters: filters ={}
	columns = ["Delivery Note:Link/Delivery Note:130","Customer:Link/Customer:200","Vehicle:Link/Vehicle:100","Driver:Link/Driver:100","Delivery Status::100"]
	conditions = ""
	if filters.get("from_date"):
		conditions += " AND vs.date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND vs.date <= %(to_date)s"
	if filters.get("customer"):
		conditions += " AND dn.customer = %(customer)s"
        if filters.get("delivery_status"):
                conditions += " AND vsd.delivery_status = %(delivery_status)s"
        data = frappe.db.sql("SELECT vsd.delivery_note,dn.customer,vs.vehicle,vs.driver,vsd.delivery_status FROM `tabVehicle Schedule Log` vs LEFT JOIN `tabVehicle Schedule Delivery` vsd ON (vs.name = vsd.parent) LEFT JOIN `tabDelivery Note` dn ON (vsd.delivery_note = dn.name) WHERE vs.docstatus=1 {0}".format(conditions),filters)
        return columns, data
