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
                    "name": "Vehicle Allocation Schedule Report",
                    "route": "query-report/Vehicle Allocation Schedule Report",
                    "doctype": "Vehicle Schedule Log",
                },
                {
                    "type": "report",
                    "name": "Goods Tracking Report",
                    "route": "query-report/Goods Tracking Report",
                    "doctype": "Vehicle Schedule ",
                },
            ]
        },
        {
            "label": _("Setup"),
            "icon": "icon-star",
            "items": [
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
