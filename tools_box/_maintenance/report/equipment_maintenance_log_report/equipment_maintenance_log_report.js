// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.query_reports["Equipment Maintenance Log Report"] = {
	"filters": [{
			"fieldname":"modified_from",
			"label": __("Modified From"),
			"fieldtype": "Datetime",
			"width": "80",
			"reqd":1,
			"default":dateutil.year_start()
		},
		{
			"fieldname":"modified_to",
			"label": __("Modified To"),
			"fieldtype": "Datetime",
			"width": "80",
			"reqd":1,
			"default":dateutil.year_end()
		},
		/**
		{
			"fieldname": "nature_of_accident",
			"label": __("Nature of Accident"),
			"fieldtype": "Select",
			"default":'',
			"options": [{ "value": "", "label": __("Nature of Accident") }]
		},
		{
			"fieldname":"fire_extinguisher",
			"label": __("Fire Extinguisher"),
			"fieldtype": "Link",
			"width": "80",
			"reqd":0,
			"options": "Fire Extinguisher",
			"filters": {}
		},
		 **/
	]
}
