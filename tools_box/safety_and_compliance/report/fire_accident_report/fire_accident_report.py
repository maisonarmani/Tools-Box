# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	""" All the report magic happens here """
	columns, data = [
		"Accident:Link/Accident:150",
		"Victim:Data:200",
		"Nature of Accident:Data:200",
		"Fire Extinguisher Used:Link/Fire Extinguisher:150",
		"Fire Extinguisher Location: Data:150",
		"Reported By:Data:100",
		"Reported Date:Data:100"
	], []

	conditions = "tabAcc.fire_related = 1" # Only Fire related accidents

	if filters.get('modified_from') and filters.get('modified_to'):
		conditions  += ' and tabAcc.prepared_date  BETWEEN \'{0}\' and \'{1}\''.format(filters.get('modified_from'),filters.get('modified_to'))
	if filters.get('fire_extinguisher'):
		conditions  += ' and tabAcc.fire_extinguisher_used = \'{0}\''.format(filters.get('fire_extinguisher'))
	if filters.get('nature_of_accident'):
		conditions  += ' and tabAcc.type_of_accident = \'{0}\''.format(filters.get('nature_of_accident'))
	if filters.get('reported_by'):
		conditions  += ' and tabAcc.prepared_by = \'{0}\''.format(filters.get('reported_by'))

	sql = '''select tabAcc.name accident,tabAcc.employee_name victim, tabAcc.type_of_accident nature_of_accident , tabAcc.fire_extinguisher_used fire_extinguisher_used,
	tabFire.location fire_extinguisher_used, tabAcc.prepared_by reported_by,tabAcc.prepared_date reported_date from `tabFire Extinguisher` tabFire LEFT JOIN `tabAccident` tabAcc
	ON (tabFire.name = tabAcc.fire_extinguisher_used) WHERE {0}'''

	frappe.errprint(sql.format(conditions))
	data = frappe.db.sql(sql.format(conditions))
	return columns,data