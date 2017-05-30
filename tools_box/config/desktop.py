# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Safety and Compliance",
			"color": "#1b623f",
			"icon": "octicon octicon-hubot",
			"type": "module",
			"label": _("Safety and Compliance")
		},
		{
			"module_name": "Logistics",
			"color": "#e7c016",
			"icon": "octicon octicon-dashboard",
			"type": "module",
			"label": _("Logistics")
		},
		{
			"module_name": "Support",
			"color": "#2c3e50",
			"icon": "fa fa-phone",
			"icon": "octicon octicon-issue-opened",
			"type": "module",
			"label": _("Support")
		},
	]
