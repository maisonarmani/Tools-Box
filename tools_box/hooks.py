# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version
from frappe import _

app_name = "tools_box"
app_title = "Tools Box"
app_publisher = "masonarmani38@gmail.com"
app_description = "Tools box contains erpnext extensions for companies"
app_icon = "octicon octicon-rocket"
app_color = "#b85423"
app_email = "masonarmani38@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tools_box/css/tools_box.css"
# app_include_js = "/assets/tools_box/js/tools_box.js"

# include js, css files in header of web template
# web_include_css = "/assets/tools_box/css/tools_box.css"
# web_include_js = "/assets/tools_box/js/tools_box.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "tools_box.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Meeting", "File"]

# Installation
# ------------

# before_install = "tools_box.install.before_install"
# after_install = "tools_box.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tools_box.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
    "Sales Invoice" : "tools_box.tools_box.doctype.administrative_zone_setup.administrative_zone_setup.get_permission_query_conditions_for_sales_invoice",
    "Sales Order" : "tools_box.tools_box.doctype.administrative_zone_setup.administrative_zone_setup.get_permission_query_conditions_for_sales_order",
    "Delivery Note" : "tools_box.tools_box.doctype.administrative_zone_setup.administrative_zone_setup.get_permission_query_conditions_for_del_note",
    "Authority to Load" : "tools_box.tools_box.doctype.administrative_zone_setup.administrative_zone_setup.get_permission_query_conditions_for_atl",
    "Customer" : "tools_box.tools_box.doctype.administrative_zone_setup.administrative_zone_setup.get_permission_query_conditions_for_customer",
}

standard_portal_menu_items = [
    #	{"title": _("Meetings"), "route": "/meetings", "reference_doctype": "Meeting"},
    #	{"title": _("Document Manager"), "route": "/documents", "reference_doctype": "File"}
]

#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {

}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "hourly": [
        "erpnext.stock.reorder_item.reorder_item"
    ],
}

# Testing
# -------

# before_tests = "tools_box.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tools_box.event.get_events"
# }
