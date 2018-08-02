# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    columns, data = get_cols(), get_data(filters.get('from'), filters.get('to'), filters.get('territory'),
                                         filters.get('customer'), filters.get('status'))
    return columns, data


def get_cols():
    return [
        "Order:Link/Sales Order:140",
        "Authority to Load:Link/Authority to Load:140",
        "Customer:Link/Customer:160",
        "Status:Data:100",
        "Transaction Date:Date:120",
        "Delivery Date:Date:120",
        "Planned Delivery Date:Date:120",
        "Territory:Link/Territory:170",
        "Total:Currency:130",
    ]


def get_data(ps, pe, territory=None, customer=None, status=None):
    conds = "AND so.name = atl.sales_order"
    if status == "Pending":
        conds += " AND so.docstatus = 1 AND  so.delivery_status = 'Not Delivered'"

    if status == "Delivered":
        conds += " AND so.docstatus = 1 AND  so.delivery_status = 'Fully Delivered'"

    if status == "Scheduled":
        conds += " AND so.docstatus = 0 AND  so.delivery_status = 'Not Delivered'"

    if status == "Overdue":
        conds += " AND so.docstatus = 1 AND DATE_ADD(atl.delivery_date,INTERVAL 2 DAY) < CURDATE()"

    if territory:
        conds += " AND so.territory = '%s' " % territory
    if customer:
        conds += " AND so.customer = '%s' " % customer

    return frappe.db.sql(
        "SELECT so.name,atl.name, so.customer , '%s' as status ,so.transaction_date, atl.delivery_date,DATE_ADD(atl.delivery_date,INTERVAL 2 DAY), so.territory, so.grand_total from "
        "`tabSales Order` so INNER JOIN `tabAuthority to Load` atl WHERE  so.docstatus = 1 AND so.transaction_date "
        "BETWEEN DATE('%s') AND DATE('%s')  %s ORDER BY so.territory " % (status, ps, pe, conds), as_list=1)
