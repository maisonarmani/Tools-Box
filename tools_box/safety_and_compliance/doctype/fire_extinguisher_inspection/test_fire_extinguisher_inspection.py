# -*- coding: utf-8 -*-
# Copyright (c) 2015, masonarmani38@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import datetime 
import unittest
from frappe.model.db_schema import type_map, varchar_len

# test_records = frappe.get_test_records('Fire Extinguisher')

class TestFireExtinguisher(unittest.TestCase):
	def test_all(self):
		print((type_map[frappe.get_meta('Job Card Material Detail').get_field('item_description').fieldtype]))

	def _test_outlet(self):
		conditions = ""
		filters = dict(
			from_date = datetime.datetime(2016,01,01),
			to_date = datetime.datetime(2017,1,30)
		)
		if filters.get("from_date"):
			conditions += " AND os.date >= '{from_date}'"
		if filters.get("to_date"):
			conditions += " AND os.date <= '{to_date}'"
		if filters.get("sales_rep"):
			conditions += " AND os.sales_rep = {sales_rep}"
		if filters.get("route"):
			conditions += " AND os.route = {route}"

		query = '''SELECT os.date,os.name,od.outlet_name,od.address,os.sales_rep,os.route, od.phone phone_number FROM `tabOutlet Survey` os, `tabOutlet Details` od WHERE os.name = od.parent {conditions}'''
		query = query.format(conditions=conditions).format(**filters)
		data = frappe.db.sql(query)
		print(data)

	def _test_fire_acccide_report(self):
    		
		filters = {
			'prepared_from':datetime.date(2017,01,13),
			'prepared_to':datetime.date(2017,1,30),
			'fire_extinguisher':'GTRC-1001',
			'nature_of_accident':'Fatal'
		}	
		
		columns, data = [
			"Accident:Link/Accident:200",
			"Victim:Data:300",
			"Nature of Accident:Data:300",
			"Fire Extinguisher Used:Link/Fire Extingusher Inspection:200",
			"Fire Extinguisher Location: Data:200",
			"Reported By:Data:200",
			"Reported Date:Data:200"
		], []
		
		conditions = "ta.fire_related = 1" # Only Fire related accidents

		if filters.get('prepared_from') and filters.get('prepared_to'):
			conditions  += ' and ta.prepared_date  BETWEEN \'{0}\' and \'{1}\''.format(filters.get('prepared_from'),filters.get('prepared_to'))

		if filters.get('fire_extinguisher'):
			conditions  += ' and ta.fire_extinguisher_used = \'{0}\''.format(filters.get('fire_extinguisher'))

		sql = '''select ta.name accident,ta.employee_name victim, ta.type_of_accident nature_of_accident , ta.fire_extinguisher_used fire_extinguisher_used,
		fei.location fire_extinguisher_used, ta.prepared_by reported_by,ta.prepared_date reported_date from `tabFire Extinguisher Inspection` fei LEFT JOIN `tabAccident` ta 
		ON (fei.reference_number = ta.fire_extinguisher_used) WHERE {0}'''

		#print(sql.format(conditions))
		#data = frappe.db.sql(sql.format(conditions), as_list=True)
		print(data)