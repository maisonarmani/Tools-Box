# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

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
# website_generators = ["Web Page"]

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

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "*": {
        "after_save": [
            "tools_box.controllers.sentinel.validate_status",
        ]
#		"after_save": "method",
#		"on_cancel": "method",
# 		"on_trash": "method"
	},
}


# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"tools_box.tasks.all"
# 	],
# 	"daily": [
# 		"tools_box.tasks.daily"
# 	],
# 	"hourly": [
# 		"tools_box.tasks.hourly"
# 	],
# 	"weekly": [
# 		"tools_box.tasks.weekly"
# 	]
# 	"monthly": [
# 		"tools_box.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "tools_box.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tools_box.event.get_events"
# }

