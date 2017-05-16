# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
        if not filters: filters ={}
        columns = [
                "Date:Datetime:110",
                "Survey ID::100",
                "Outlet Name:Data:100",
                "Outlet Location:Data:200",
                "Sales Rep:Link/Sales Person:100",
                "Route:Link/Territory:100",
                "Phone Number:Data:100"
        ]
        conditions = ""
        if filters.get("from_date"):
                conditions += " AND os.date >= '{from_date}'"
        if filters.get("to_date"):
                conditions += " AND os.date <= '{to_date}'"
        if filters.get("sales_rep"):
                conditions += " AND os.sales_rep = '{sales_rep}'"
        if filters.get("route"):
                conditions += " AND os.route = '{route}'"

        query = '''SELECT os.date,os.name,od.outlet_name,od.address,os.sales_rep,os.route, od.phone phone_number FROM `tabOutlet Survey` os, `tabOutlet Details` od WHERE os.name = od.parent {conditions}'''
        query = query.format(conditions=conditions).format(**filters)
        print(query)
        data = frappe.db.sql(query)
        return columns, data
