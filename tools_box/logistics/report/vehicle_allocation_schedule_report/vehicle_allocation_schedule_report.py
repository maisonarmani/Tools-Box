# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    if not filters: filters = {}
    columns = ["Date:Date:100", "VS Doc ID:Link/Vehicle Schedule Log:130", "Vehicle:Link/Vehicle:100",
               "Driver:Link/Driver:100", "Sales Rep:Link/Sales Person:200", "Delivery Note:Link/Delivery Note:200",
               "Total:Currency:200"]
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND vs.date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND vs.date <= %(to_date)s"
    if filters.get("vehicle"):
        conditions += " AND vs.vehicle = %(vehicle)s"
    if filters.get("driver"):
        conditions += " AND vs.driver = %(driver)s"
    if filters.get("delivery_note"):
        conditions += " AND vsd.delivery_note = %(delivery_note)s"
    data = frappe.db.sql(
        "SELECT vs.date,vs.name,vs.vehicle,vs.driver,vs.sales_rep,vsd.delivery_note,dn.grand_total FROM ("
        "`tabVehicle Schedule Log` vs LEFT JOIN `tabVehicle Schedule Delivery` vsd ON (vs.name = vsd.parent)) "
        "LEFT OUTER JOIN  `tabDelivery Note` dn  ON (dn.name = vsd.delivery_note) WHERE vs.docstatus=1 {0}".format(
            conditions), filters)
    return columns, data
