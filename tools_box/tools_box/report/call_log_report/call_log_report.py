# Copyright (c) 2013, bobzz.zone@gmail.com , masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


# Date	Customer 	Call Type	Purpose of Call ( We would add as applicable) 	Customers Comment	Sales Admin Remark/ Resolution

def execute(filters=None):
    columns, data = ["Date:Datetime:200", "Call Log:Link/Call Log:150", "Customer:Link/Customer:200",
                     "Call Type:Data:100",
                     "Purpose of Call:Data:150", "Customer Comment:Data:300", "Sales Admin Remark:Data:400",
                     "Caller::200"], []
    conditions = " (date between '{from}' and '{to}') "

    if filters.get("customer"):
        conditions += """ and customer = "{customer}" """
    if filters.get("call_type"):
        conditions += """ and call_type = "{call_type}" """
    if filters.get("call_purpose"):
        conditions += """ and call_purpose = "{call_purpose}" """

    data = frappe.db.sql("""select cl.date,cl.name, cl.customer, cl.call_type,cl.call_purpose,cl.customer_comment,cl.sales_admin_remark,emp.employee_name
	      from `tabCall Log` cl INNER JOIN `tabEmployee` emp ON(cl.owner = emp.user_id) WHERE cl.docstatus=1 and {0}  """.format(conditions.format(**filters)), as_list=1)

    return columns, data
