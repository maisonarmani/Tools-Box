# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    # get all production order for an item or items in a particular item group
    # run them tru what is suppose to be produced and what has been produced for each production order
    # go to stock entry and get the item that was actually manufactured
    # check the stock entry item where def target warehouse != ""
    # and the item is the item to be produced

    # local global
    production_order = ""
    data = []
    columns = [
        "Date:Date:120",
        "Item Code:Link/Item:100",
        "Item Name:Data:160",
        "Item Group:Data:100",
        "UOM:Link/UOM:75",
        "Production Order:Link/Production Order:160",
        "Expected Output:Float:100",
        "Actual Output:Float:100",
        "Variance:Float:100"
    ]

    def get_excess():
        excess = 0
        if production_order:
            fgtf = frappe.db.sql("""select sum(c.qty) excess from `tabFinished Goods Transfer Form` p  JOIN
                      `tabFinished Goods Transfer Item` c ON p.name = c.parent  WHERE p.weekly_production_order_form = '%s'
                        GROUP BY weekly_production_order_form""" % production_order, as_list=1)
            if len(fgtf):
                excess = fgtf[0][0]

        return excess

    def get_considered_items(item_group=None, item=None, production_order=None):

        filters = {}


        if production_order != None:
            # get producion item
            item = frappe.db.sql("select production_item from `tabProduction Order` where name='%s'" %production_order, as_dict=1)

            filters.update({"name": item[0].production_item})

        elif item != None:
            filters.update({"name": item})

        if item_group != None:
            filters.update({"item_group": item_group})
        frappe.errprint(filters)

        items = frappe.get_list(doctype="Item", filters=filters,
                                fields=['name', 'stock_uom', 'item_name', 'item_group'])
        return items


    def get_production_orders(item=None, **kwargs):
        if item != None:
            production_orders = frappe.db.sql(
                """select name,planned_start_date, production_item,qty, produced_qty from `tabProduction Order` where production_item='{item}'  and planned_start_date
                BETWEEN DATE('{start_date}') and DATE('{end_date}') and status='Completed' """.format(item=item,
                                                                                                      **kwargs),
                as_dict=1)
        else:
            production_orders = frappe.db.sql(
                """select name, planned_start_date,production_item,qty, produced_qty from `tabProduction Order` where  planned_start_date BETWEEN
                        DATE('{start_date}') and DATE('{end_date}') and status='Completed' """.format(**kwargs),
                as_dict=1)
        return production_orders

    items = []
    # start date and end date
    sd, ed = filters.get("from"), filters.get("to")

    if filters.get("item") != None:
        items = get_considered_items(item=filters.get("item"))

    elif filters.get("item_group") != None:
        items = get_considered_items(item_group=filters.get("item_group"))

    elif filters.get("production_order") != None:
        items = get_considered_items(production_order=filters.get("production_order"))

    if len(items) > 0:
        for item in items:
            production_orders = get_production_orders(start_date=sd, end_date=ed, item=item.name)
            for po in production_orders:
                production_order = po.name
                expected = po.qty
                actual = po.produced_qty
                excess = get_excess()
                data.append(
                    (po.planned_start_date, item.name, item.item_name, item.item_group,item.stock_uom,po.name,
                     expected, actual + excess, - expected + (actual + excess))
                )
    else:
        production_orders = get_production_orders(start_date=sd, end_date=ed)
        for po in production_orders:
            production_order = po.name
            expected = po.qty
            actual = po.produced_qty
            excess = get_excess()
            item = get_considered_items(item=po.production_item)[0]
            data.append(
                (po.planned_start_date, item.name, item.item_name, item.item_group, item.stock_uom,po.name,
                 expected, actual + excess, - expected + (actual + excess))
            )
    return columns, data
