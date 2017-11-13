# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cint, flt, cstr, comma_or

""" 
    This is suppose to return some kind of information used as addon
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
        "label": _("Authority to Load"),
        "name": "Authority to Load",
        "icon": "icon-sitemap",
        "link": "List/Authority to Load",
        "description": _("Authority to Load"),
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
    }, {
        "type": "doctype",
        "label": _("Sales Journey Plan"),
        "name": "Sales Journey Plan",
        "icon": "icon-sitemap",
        "link": "List/Sales Journey Plan",
        "description": _("Sales Journey Plan."),
    }, {
        "type": "doctype",
        "label": _("Sales Weekly Report"),
        "name": "Sales Weekly Report",
        "icon": "icon-sitemap",
        "link": "List/Sales Weekly Report",
        "description": _("Sales Weekly Report."),
    }, {
        "type": "doctype",
        "label": _("Sales Weekly Report Setup"),
        "name": "Sales Weekly Report Config",
        "icon": "icon-sitemap",
        "link": "List/Sales Weekly Report Config",
        "description": _("Sales Weekly Report Config."),
    }])


def get_account_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Petty Cash Log"),
        "name": "Petty Cash Log",
        "icon": "icon-sitemap",
        "link": "List/Petty Cash Log",
        "description": _("Petty Cash Log"),
    }, {
        "type": "doctype",
        "label": _("Payment Voucher Form"),
        "name": "Payment Voucher Form",
        "icon": "icon-sitemap",
        "link": "List/Payment Voucher Form",
        "description": _("Payment Voucher Form"),
    }, {
        "type": "doctype",
        "label": _("Asset Transfer Form"),
        "name": "Asset Transfer Form",
        "icon": "icon-sitemap",
        "link": "List/Asset Transfer Form",
        "description": _("Asset Transfer Form"),
    }], label="Additional")


def get_stock_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Quality Control Material Acceptance Form"),
        "name": "Quality Control Material Acceptance Form",
        "icon": "icon-sitemap",
        "link": "List/Quality Control Material Acceptance Form",
        "description": _("Quality Control Material Acceptance Form"),
    }, {
        "type": "doctype",
        "label": _("Store Bin Card"),
        "name": "Store Bin Card",
        "icon": "icon-sitemap",
        "link": "List/Store Bin Card",
        "description": _("Store Bin Card"),
    },{
        "type": "doctype",
        "label": _("Stationaries Request"),
        "name": "Stationaries Request",
        "icon": "icon-sitemap",
        "link": "List/Stationaries Request",
        "description": _("Stationaries Request"),
    } ])


def get_production_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Raw Materials Return Form"),
        "name": "Raw Materials Return Form",
        "icon": "icon-sitemap",
        "link": "List/Raw Materials Return Form",
        "description": _("Raw Materials Return Form"),
    }, {
        "type": "doctype",
        "label": _("Finished Goods Transfer Form"),
        "name": "Finished Goods Transfer Form",
        "icon": "icon-sitemap",
        "link": "List/Finished Goods Transfer Form",
        "description": _("Finished Goods Transfer Form"),
    },
    ], label="Additional")


def get_waste_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Production Waste"),
        "name": "Production Waste",
        "icon": "icon-sitemap",
        "link": "List/Production Waste",
        "description": _("Production Waste"),
    }, {
        "type": "doctype",
        "label": _("Waste Sold"),
        "name": "Production Waste",
        "icon": "icon-sitemap",
        "link": "List/Sold Waste",
        "description": _("Sold Waste"),
    }, {
        "type": "doctype",
        "label": _("Waste Control Inspection"),
        "name": "Waste Control Inspection",
        "icon": "icon-sitemap",
        "link": "List/Waste Control Inspection",
        "description": _("Waste Control Inspection"),
    }, {
        "type": "doctype",
        "label": _("Production Waste Setup"),
        "name": "Production Waste Setup",
        "icon": "icon-sitemap",
        "link": "List/Production Waste Setup",
        "description": _("Production Waste Setup"),
    }, {
        "type": "doctype",
        "label": _("Machine Downtime Monitoring"),
        "name": "Machine Downtime Monitoring",
        "icon": "icon-sitemap",
        "link": "List/Machine Downtime Monitoring",
        "description": _("Machine Downtime Monitoring"),
    }], label="Production Waste")


def get_maintenance_section():
    return __default_item([
        {
            "type": "doctype",
            "label": _("Equipment Maintenance Log"),
            "name": "Equipment Maintenance Log",
            "icon": "icon-sitemap",
            "link": "List/Equipment Maintenance Log",
            "description": _("Equipment Maintenance Log"),
        },
        {
            "type": "doctype",
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
    return __default_item([
        {
            "type": "doctype",
            "label": _("Purchase Requisition"),
            "name": "Purchase Requisition",
            "icon": "icon-sitemap",
            "link": "List/Purchase Requisition",
            "description": _("Purchase Requisition"),
        }
    ], label="Additionals")


def get_hr_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Staff Requisition Form"),
        "name": "Staff Requisition Form",
        "icon": "icon-sitemap",
        "link": "List/Staff Requisition Form",
        "description": _("Staff Requisition Form"),
    }, {
        "type": "doctype",
        "label": _("Staff Replacement Request Form"),
        "name": "Staff Replacement Request Form",
        "icon": "icon-sitemap",
        "link": "List/Staff Replacement Request Form",
        "description": _("Staff Replacement Request Form"),
    }, {
        "type": "doctype",
        "label": _("Overtime Request"),
        "name": "Overtime Request",
        "icon": "icon-sitemap",
        "link": "List/Overtime Request",
        "description": _("Overtime Request"),
    }, {
        "type": "doctype",
        "label": _("Overtime Sheet"),
        "name": "Overtime Sheet",
        "icon": "icon-sitemap",
        "link": "List/Overtime Sheet",
        "description": _("Overtime Sheet"),
    }, {
        "type": "doctype",
        "label": _("Stationaries Request"),
        "name": "Stationaries Request",
        "icon": "icon-sitemap",
        "link": "List/Stationaries Request",
        "description": _("Stationaries Request"),
    },{
        "type": "doctype",
        "label": _("Stationaries Log"),
        "name": "Stationaries Log",
        "icon": "icon-sitemap",
        "link": "List/Stationaries Log",
        "description": _("Stationaries Log"),
    },
    ])


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


def get_extra_waste_reports():
    return __default_rep_items([{
        "type": "report",
        "name": "Production Waste Report",
        "doctype": "Production Waste",
        "is_query_report": True,
    }, {
        "type": "report",
        "name": "Sold Waste Report",
        "doctype": "Sold Waste",
        "label": "Waste Sold Report",
        "is_query_report": True,
    }
    ], label="Production Waste Reports")


def get_extra_production_reports():
    return __default_rep_items([
        {
            "type": "report",
            "name": "Finished Goods Transfer Report",
            "doctype": "Finished Goods Transfer Form",
            "is_query_report": True,
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
        }, {
            "type": "report",
            "name": "Production Yield Variance Report",
            "doctype": "Production Order",
            "is_query_report": True,
        },
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
            "name": "Generator Fuel Consumption Log Report",
            "doctype": "Generator Fuel Consumption Log",
            "is_query_report": False,
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
        },
        {
            "type": "report",
            "name": "Equipment Maintenance Log Report",
            "doctype": "Equipment Maintenance Log Report",
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
            "name": "Sales Weekly Report",
            "route": "query-report/Sales Weekly Report",
            "doctype": "Sales Weekly Report",
        },
        {
            "type": "report",
            "name": "Outlet Survey Report",
            "route": "query-report/Outlet Survey Report",
            "doctype": "Outlet Survey",
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
            "doctype": "Sales Invoice"
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
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Purchase Requisition Report",
            "doctype": "Purchase Requisition"
        },

        {
            "type": "report",
            "is_query_report": True,
            "name": "Material Request Report",
            "doctype": "Material Request"
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
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Stock Balance With Valuation",
            "doctype": "Stock Entry",
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


def __default_item(items, label="Extras"):
    return {
        "label": label,
        "items": items,
        "icon": "icon-cog"
    }


def __default_rep_items(items, label="Extra Reports"):
    return {
        "label": label,
        "items": items
    }
