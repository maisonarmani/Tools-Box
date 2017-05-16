# Copyright (c) 2013, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    # Item Code	Asset Name	Asset Catergory	Warehouse	Purchase Date	Value (After Depreciation)
    columns, data = [
                        "Item Code:Link/Item:200",
                        "Asset Name::200",
                        "Asset Category:Link/Asset Category:200",
                        "Warehouse:Link/Warehouse:200",
                        "Purchase Date:Date:200",
                        "Book Value:Currency:200"], []
    where = ""
    if filters.get("asset_category"):
        where = """ and tA.asset_category = "{}" """.format(filters.get("asset_category"))
    if filters.get('include_custodian'):
        columns += ["Custodian - Employee ::200","Custodian - Department:Link/Department:150"]

    data = frappe.db.sql("""select tA.item_code,tA.name,tA.asset_category,tA.warehouse,tA.purchase_date,
        tA.value_after_depreciation, tA.custodian_employee_name, tA.custodian_department from tabAsset tA 
        where tA.docstatus=1 {}""".format(where), as_list=1)
    return columns, data
