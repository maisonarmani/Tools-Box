 # Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint
from frappe import _


def execute(filters=None):
    if not filters: filters = {}

    days_since_last_order = filters.get("days_since_last_order")
    doctype = filters.get("doctype")

    if cint(days_since_last_order) <= 0:
        frappe.throw(_("'Days Since Last Order' must be greater than or equal to zero"))

    columns = get_columns(filters.doctype)
    customers = get_sales_details(doctype)

    data = []
    for cust in customers:
        if cint(cust[8]) >= cint(days_since_last_order):
            cust.insert(7, get_last_sales_amt(cust[0], doctype))
            data.append(cust)
    return columns, data


def get_sales_details(doctype):
    cond = """sum(so.base_net_total) as 'total_order_considered',
			max(so.posting_date) as 'last_order_date',
			DATEDIFF(CURDATE(), max(so.posting_date)) as 'days_since_last_order' """
    if doctype == "Sales Order":
        cond = """sum(if(so.status = "Stopped",
				so.base_net_total * so.per_delivered/100,
				so.base_net_total)) as 'total_order_considered',
			max(so.transaction_date) as 'last_order_date',
			DATEDIFF(CURDATE(), max(so.transaction_date)) as 'days_since_last_order'"""

    return frappe.db.sql("""select
			cust.name,
			cust.customer_name,
			cust.territory,
			cust.customer_group,
			count(distinct(so.name)) 'num_of_order',
			sum(base_net_total) 'total_order_value', {0}
		from `tabCustomer` cust  right outer join `tab{1}` so on(cust.name = so.customer)
		where so.docstatus = 1 group by cust.name
		order by 'days_since_last_order' desc """.format(cond, doctype), as_list=1)


def get_last_sales_amt(customer, doctype):
    cond = "posting_date"
    if doctype == "Sales Order":
        cond = "transaction_date"
    res = frappe.db.sql("""select base_net_total from `tab{0}`
		where customer = %s and docstatus = 1 order by {1} desc
		limit 1""".format(doctype, cond), customer)

    return res and res[0][0] or 0

def get_columns(doctype):
	_doctype = "Invoice"
	if doctype == "Sales Order":
		_doctype = "Order"

	return [
		_("Customer") + ":Link/Customer:120",
		_("Customer Name") + ":Data:120",
		_("Territory") + "::120",
		_("Customer Group") + "::120",
		_("Number of {0}").format(_doctype) + "::120",
		_("Total {0} Value").format(_doctype) + ":Currency:120",
		_("Total {0} Considered").format(_doctype) + ":Currency:160",
		_("Last {0} Amount").format(_doctype) + ":Currency:160",
		_("Last {0} Date").format(_doctype) + ":Date:160",
		_("Days Since Last {0}").format(_doctype) + "::160"
	]
