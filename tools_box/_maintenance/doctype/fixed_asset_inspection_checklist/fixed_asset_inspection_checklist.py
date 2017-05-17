# -*- coding: utf-8 -*-
# Copyright (c) 2015, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FixedAssetInspectionChecklist(Document):
	pass
def get_asset_with_category(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""
		select asset_name
		from tabAsset
		where 
		docstatus = 1 and asset_name like %s and asset_category = "{}"
	""".format(filters.get("category")), ("%" + txt + "%"))