# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cint, flt, cstr, comma_or

""" 
    this is suppose to return some kind of information used as addon
    the Goal is to maintain all icons that's not ERPNext's from a centralized location
    thus making it easy to amend or extend
"""


def get_selling_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Call Log"),
        "name": "Call Log",
        "icon": "icon-sitemap",
        "link": "List/Call Log",
        "description": _("Manage Call Log."),
    }, {
        "type": "doctype",
        "label": _("Competitor"),
        "name": "Competitor",
        "icon": "icon-sitemap",
        "link": "List/Competitor",
        "description": _("Manage Competitors."),
    }, {
        "type": "doctype",
        "label": _("Outlet Survey"),
        "name": "Outlet Survey",
        "icon": "icon-sitemap",
        "link": "List/Outlet Survey",
        "description": _("Outlet Survey."),
    }, {
        "type": "doctype",
        "label": _("Performance Assessment Form"),
        "name": "Performance Assessment Form",
        "icon": "icon-sitemap",
        "link": "List/Performance Assessment Form",
        "description": _("Performance Assessment Form."),
    }, {
        "type": "doctype",
        "label": _("Daily Route Activity"),
        "name": "Daily Route Activity",
        "icon": "icon-sitemap",
        "link": "List/Daily Route Activity",
        "description": _("Daily Route Activity."),
    }, ])


def get_account_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Petty Cash Log"),
        "name": "Petty Cash Log",
        "icon": "icon-sitemap",
        "link": "List/Petty Cash Log",
        "description": _("Petty Cash Log"),
    },{
        "type": "doctype",
        "label": _("Petty Voucher Form"),
        "name": "Petty Voucher Form",
        "icon": "icon-sitemap",
        "link": "List/Petty Voucher Form",
        "description": _("Petty Voucher Form"),
    }])


def get_stock_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Finish Goods Transfer Form"),
        "name": "Finish Goods Transfer Form",
        "icon": "icon-sitemap",
        "link": "List/Finish Goods Transfer Form",
        "description": _("Finish Goods Transfer Form"),
    }, {
        "type": "doctype",
        "label": _("Quality Control Material Acceptance Form"),
        "name": "Quality Control Material Acceptance Form",
        "icon": "icon-sitemap",
        "link": "List/Quality Control Material Acceptance Form",
        "description": _("Quality Control Material Acceptance Form"),
    }, ])


def get_production_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Production Unit"),
        "name": "Production Unit",
        "icon": "icon-sitemap",
        "link": "List/Production Unit",
        "description": _("Production Unit"),
    }, {
        "type": "doctype",
        "label": _("Production Yield Control Form"),
        "name": "Production Yield Control Form",
        "icon": "icon-sitemap",
        "link": "List/Production Yield Control Form",
        "description": _("Production Yield Control Form"),
    }, {
        "type": "doctype",
        "label": _("Weekly Production Plan"),
        "name": "Weekly Production Plan",
        "icon": "icon-sitemap",
        "link": "List/Weekly Production Plan",
        "description": _("Weekly Production Plan"),
    }])


def get_maintenance_section():
    return __default_item([
        {
            "type": "doctype" ,
            "label": _("Computing Asset Inspection Checklist"),
            "name": "Computing Asset Inspection Checklist",
            "icon": "icon-sitemap",
            "link": "List/Computing Asset Inspection Checklist",
            "description": _("Computing Asset Inspection Checklist"),
        },
        {
            "type": "doctype",
            "label": _("Fixed Asset Inspection Checklist"),
            "name": "Fixed Asset Inspection Checklist",
            "icon": "icon-sitemap",
            "link": "List/Fixed Asset Inspection Checklist",
            "description": _("Fixed Asset Inspection Checklist"),
        },
        {
            "type": "doctype",
            "label": _("Generator Fuel Consumption Log"),
            "name": "Generator Fuel Consumption Log",
            "icon": "icon-sitemap",
            "link": "List/Generator Fuel Consumption Log",
            "description": _("Generator Fuel Consumption Log"),
        },
        {
            "type": "doctype",
            "label": _("Daily Generator Activity Log"),
            "name": "Daily Generator Activity Log",
            "icon": "icon-sitemap",
            "link": "List/Daily Generator Activity Log",
            "description": _("Daily Generator Activity Log"),
        }
    ])

def get_purchasing_section():
    return __default_item([{}])


def get_hr_section():
    return __default_item([{}])


def get_support_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Helpdesk Ticket"),
        "name": "Helpdesk Ticket",
        "icon": "icon-sitemap",
        "link": "List/Helpdesk Ticket",
        "description": _("Helpdesk Ticket"),
    }, {
        "type": "doctype",
        "label": _("Job Card"),
        "name": "Job Card",
        "icon": "icon-sitemap",
        "link": "List/Job Card",
        "description": _("Job Card"),
    }])


def get_extra_hr_reports():
    return __default_rep_items([
        {
            "type": "report",
            "name": "Expense Claim Report",
            "doctype": "Expense Claim",
            "is_query_report": True,
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Employee Leave Balance",
            "doctype": "Leave Application"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Employee Birthday",
            "doctype": "Employee"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Employees working on a holiday",
            "doctype": "Employee"
        },
        {
            "type": "report",
            "name": "Employee Status Summary",
            "doctype": "Employee",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Employee Report Summary",
            "doctype": "Employee",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Employee Information",
            "doctype": "Employee"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Monthly Salary Register",
            "doctype": "Salary Slip"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Monthly Attendance Sheet",
            "doctype": "Attendance"
        }, ])


def get_extra_production_reports():
    return __default_rep_items([{
        "type": "report",
        "name": "Finished Goods Transfer Report",
        "doctype": "Finished Goods Transfer Form",
        "is_query_report": True,
    }, {
        "type": "report",
        "name": "Production Order Report",
        "doctype": "Weekly Production Order Form",
        "is_query_report": True,
    }, {
        "type": "report",
        "name": "Production Yield Variance Report",
        "doctype": "Production Yield Control Form",
        "is_query_report": True,
    }, {
        "type": "report",
        "name": "Raw Materials Return Report",
        "doctype": "Raw Materials Return Form",
        "is_query_report": True,
    }
    ])


def get_extra_maintenance_reports():
    return __default_rep_items([
        {
            "type": "report",
            "name": "Daily Generator Activity Log Report",
            "doctype": "Daily Generator Activity Log",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Generator Fuel Consumption Report",
            "doctype": "Generator Fuel Consumption",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Fixed Asset Inspection Checklist Report",
            "doctype": "Fixed Asset Inspection Checklist",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Computing Asset Inspection Checklist Report",
            "doctype": "Computing Asset Inspection Checklist",
            "is_query_report": True,
        }
    ])


def get_extra_account_reports():
    return __default_rep_items([
        {

            "type": "report",
            "name": "Bank Balance Report",
            "doctype": "Journal Entry",
            "is_query_report": True,
        }, {

            "type": "report",
            "name": "Payment Voucher Report",
            "doctype": "Payment Voucher Form",
            "is_query_report": True,
        }, {

            "type": "report",
            "name": "Payment Entry Report",
            "doctype": "Payment Entry",
            "is_query_report": True,
        }, {

            "type": "report",
            "name": "Petty Cash Log Report",
            "doctype": "Petty cash Log",
            "is_query_report": True,
        }
    ])


def get_extra_selling_reports():
    return __default_rep_items([
        {
            "type": "report",
            "name": "Call Log Report",
            "is_query_report": True,
            "doctype": "Call Log",
        },
        {
            "type": "report",
            "name": "Daily Route Activity Report",
            "route": "query-report/Daily Route Activity Report",
            "doctype": "Daily Route Activity",
        },
        {
            "type": "report",
            "name": "Customer Commission Report",
            "route": "query-report/Customer Commission Report",
            "doctype": "Sales Invoice",
        },
        {
            "type": "report",
            "name": "Customer Commission Report Simplified",
            "route": "query-report/Customer Commission Report Simplified",
            "doctype": "Sales Invoice",
        },
        {
            "type": "report",
            "name": "Sales Rep Scorecard Report",
            "route": "query-report/Sales Rep Scorecard Report",
            "doctype": "Sales Invoice",
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Product Delivery & Distribution Schedule Report",
            "doctype": "Sales Order"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Sales By Product Report",
            "doctype": "Sales Order"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Sales By Product Report Summary",
            "doctype": "Sales Order"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Inactive Customers",
            "doctype": "Sales Order"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Customer Credit Balance",
            "doctype": "Customer"
        },
        {
            "type": "report",
            "name": "Sales Person-wise Transaction Summary",
            "doctype": "Sales Order",
            "is_query_report": True,
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Sales Variance Report",
            "doctype": "Sales order"
        }, {
            "type": "report",
            "name": "Overdue Sales Invoice",
            "doctype": "Sales Invoice",
            "is_query_report": True,
        }])


def get_extra_purchase_reports():
    return __default_rep_items([
        {
            "type": "report",
            "name": "Overdue Purchase Invoice",
            "doctype": "Purchase Invoice",
            "is_query_report": True,
        }, {
            "type": "report",
            "is_query_report": True,
            "name": "Purchase Order Status Report",
            "doctype": "Purchase Order Status"
        }, {
            "type": "report",
            "is_query_report": True,
            "name": "Purchase by Items Report Summary",
            "doctype": "Purchase Invoice"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Purchase by Items Report Details",
            "doctype": "Purchase Invoice"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Purchase Order Summary Report",
            "doctype": "Purchase Order"
        }
    ])


def get_extra_stock_reports():
    return __default_rep_items([
        {
            "type": "report",
            "is_query_report": True,
            "name": "Stock Ledger Simplified",
            "doctype": "Stock Ledger Entry",
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Raw material re-order Report",
            "doctype": "Item",
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Raw Materials Return Report",
            "doctype": "Raw Materials Return Form",
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Store Bin Cards Report",
            "doctype": "Store Bin Card",
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Stock Count Report",
            "doctype": "Stock Ledger Entry",
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Material Receipt List Report",
            "doctype": "Purchase Receipt",
        }
    ])


def get_extra_support_reports():
    return __default_rep_items([
        {
            "type": "report",
            "name": "HelpDesk Report",
            "doctype": "Helpdesk Ticket",
            "is_query_report": True
        },
        {
            "type": "report",
            "name": "Job Card Status Report",
            "doctype": "Job Card",
            "is_query_report": True
        },
        {
            "type": "report",
            "name": "Job Card Cost Report",
            "doctype": "Job Card",
            "is_query_report": True
        },
        {
            "type": "report",
            "name": "Job Card Completion Report",
            "doctype": "Job Card",
            "is_query_report": True
        },
    ])


def __default_item(items):
    return {
        "label": _("Extras"),
        "icon": "icon-cog",
        "items": items
    }


def __default_rep_items(items):
    return {
        "label": _("Extra Reports"),
        "items": items
    }
