from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
            "label": _("Forms"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Accident",
                    "description": _("Accident")
                },
                {
                    "type": "doctype",
                    "name": "Fire Accident Form",
                    "description": _("Fire Accident Form")
                },
                {
                    "type": "doctype",
                    "name": "Health Survey",
                    "description": _("Health Survey")
                },
                {
                    "type": "doctype",
                    "name": "Head Count",
                    "description": _("Head Count")
                },
                {
                    "type": "doctype",
                    "name": "Contractor Work Permit",
                    "description": _("Contractor Work Permit")
                },
                {
                    "type": "doctype",
                    "name": "Contractor Work Permit Application",
                    "description": _("Contractor Work Permit Application")
                },
                {
                    "type": "doctype",
                    "name": "Fire Extinguisher",
                    "description": _("Fire Extinguisher")
                },
                {
                    "type": "doctype",
                    "name": "Incident Report",
                    "description": _("Incident Report")
                },
            ]
        },
        {
            "label": _("Inspections"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Fire Extinguisher Inspection",
                    "description": _("Fire Extinguisher Inspection")
                },
                {
                    "type": "doctype",
                    "name": "Vehicle Safety Inspection Checklist",
                    "description": _("Vehicle Safety Inspection Checklist")

                },
                {
                    "type": "doctype",
                    "name": "Safety Inspection Checklist",
                    "description": _("Safety Inspection Checklist")
                },
                {
                    "type": "doctype",
                    "name": "Safety Checklist",
                    "description": _("Safety Checklist")
                },
            ]
        },
        {
            "label": _("Reports"),
            "items": [
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Fire Accident Report",
                    "doctype": 'Accident',
                    "description": _("Fire Accident Report")
                },
            ]
        },
        {
            "label": _("Other Reports"),
            "items": [
                {
                    "type": "report",
                    "is_query_report": False,
                    "name": "Accident Report",
                    "doctype": 'Accident',
                    "description": _("Accident Report")
                },
            ]
        }
    ]
