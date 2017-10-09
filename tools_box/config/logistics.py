from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
            "label": _("Fleet Management"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Vehicle"
                },
                {
                    "type": "doctype",
                    "name": "Vehicle Log"
                },
                {
                    "type": "doctype",
                    "name": "Vehicle Schedule",
                    "description": _("Vehicle Schedule"),
                },
                {
                    "type": "doctype",
                    "name": "Logistics Accident",
                    "description": _("Logistics Accident"),
                },
            ]
        },
        {
            "label": _("Vehicle"),
            "icon": "icon-star",
            "items": [
                {
                    "type": "doctype",
                    "name": "Vehicle Schedule Log",
                    "description": _("Vehicle Schedule Log"),
                },
                {
                    "type": "doctype",
                    "name": "Vehicle Daily Cost",
                    "description": _("Vehicle Daily Cost"),
                },
                {
                    "type": "doctype",
                    "name": "Vehicle Inspection Checklist",
                    "description": _("Vehicle Inspection Checklist"),
                },
            ]
        },
        {
            "label": _("Reports"),
            "items": [
                {
                    "type": "report",
                    "name": "Vehicle Log Report",
                    "route": "query-report/Vehicle Log Report",
                    "doctype": "Vehicle Log",
                },
                {
                    "type": "report",
                    "name": "Vehicle Schedule Report",
                    "route": "query-report/Vehicle Schedule Report",
                    "doctype": "Vehicle Schedule",
                },
                {
                    "type": "report",
                    "name": "Vehicle Allocation Schedule Report",
                    "route": "query-report/Vehicle Allocation Schedule Report",
                    "doctype": "Vehicle Schedule Log",
                },
                {
                    "type": "report",
                    "name": "Goods Tracking Report",
                    "route": "query-report/Goods Tracking Report",
                    "doctype": "Vehicle Schedule Log",
                },
                {
                    "type": "report",
                    "name": "Logistics Accident Report",
                    "route": "query-report/Logistics Accident Report",
                    "doctype": "Logistics Accident",
                },
            ]
        },
        {
            "label": _("Setup"),
            "icon": "icon-star",
            "items": [
                {
                    "type": "doctype",
                    "name": "Logistics Settings",
                    "description": _("Logistics Settings"),
                },
                {
                    "type": "doctype",
                    "name": "Driver",
                    "description": _("Driver"),
                },
                {
                    "type": "doctype",
                    "name": "Purpose",
                    "description": _("Purpose"),
                },
            ]
        },

    ]
