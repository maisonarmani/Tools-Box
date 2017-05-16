from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
            "label": _("Production Reports"),
            "items": [
                {
                    "type": "report",
                    "name": "Finished Goods Transfer Report",
                    "doctype": "Finished Goods Transfer Form",
                    "is_query_report": True,
                },
                {
                    "type": "report",
                    "name": "Production Order Report",
                    "doctype": "Weekly Production Order Form",
                    "is_query_report": True,
                },
                {
                    "type": "report",
                    "name": "Production Yield Variance Report",
                    "doctype": "Production Yield Control Form",
                    "is_query_report": True,
                },
                {
                    "type": "report",
                    "name": "Raw Materials Return Report",
                    "doctype": "Raw Materials Return Form",
                    "is_query_report": True,
                }
            ]
        }]
