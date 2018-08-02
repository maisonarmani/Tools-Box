# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from datetime import date
import frappe


def execute(filters=None):
    columns, data = get_cols(filters.get('inc_itm_qty')), get_data(ps=filters.get('from'), pe=filters.get('to'),
                                                                   territory=filters.get('territory'),
                                                                   customer=filters.get('customer'),
                                                                   inc_itm_qty=filters.get('inc_itm_qty'),
                                                                   status="Pending")

    return columns, data


def get_cols(inc_itm_qty):
    if inc_itm_qty:
        return [
            "Order:Link/Sales Order:140",
            "Customer:Link/Customer:160",
            "Item Code:Link/Item:100",
            "Item Name:Data:160",
            "Qty:Float:60",
            "Order Date:Date:120",
            "Due Delivery Date:Date:120",
            "Territory:Link/Territory:170",
        ]
    else:
        return [
            "Order:Link/Sales Order:140",
            "Customer:Link/Customer:160",
            "Order Date:Date:120",
            "Due Delivery Date:Date:120",
            "Territory:Link/Territory:170",
        ]


def get_data(ps, pe, territory=None, customer=None, status="Pending", inc_itm_qty=None):
    # fUAG = date(2018, 8, 1)
    # if ps is not None:
    # if date.strftime(ps,'%d-%-m-%Y') < fUAG:
    #    ps = fUAG

    conds = ""
    if status == "Pending":
        conds += " AND atl.docstatus = 1 AND  so.delivery_status != 'Fully Delivered'"

    if status == "Delivered":
        conds += " AND atl.docstatus = 1 AND  so.delivery_status = 'Fully Delivered'"

    if status == "Scheduled":
        conds += " AND atl.docstatus = 0 AND  so.delivery_status = 'Not Delivered'"

    if status == "Overdue":
        conds += " AND atl.docstatus = 1 AND DATE_ADD(atl.transaction_date,INTERVAL 2 DAY) < CURDATE()"

    if territory:
        conds += " AND so.territory = '%s' " % territory
    if customer:
        conds += " AND so.customer = '%s' " % customer

    sel, join = "", ""
    if inc_itm_qty:
        sel += ", ch.item_code, ch.item_name,ch.qty "
        join += " INNER JOIN`tabSales Order Item` ch ON(so.name=ch.parent)"


    return frappe.db.sql(
        "SELECT so.name,so.customer %s ,so.transaction_date, DATE_ADD(atl.transaction_date,INTERVAL 2 DAY), so.territory  from "
        "`tabSales Order` so %s INNER JOIN `tabAuthority to Load` atl ON(so.name=atl.sales_order) WHERE  so.docstatus = 1 AND DATE_ADD(so.transaction_date,INTERVAL 2 DAY) "
        "BETWEEN DATE('%s') AND DATE('%s')  %s ORDER BY so.territory " % (sel, join, ps, pe, conds), as_list=1)
