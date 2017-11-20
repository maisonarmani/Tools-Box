# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

@frappe.whitelist()
def get_active_employees(doctype, txt, searchfield, start, page_len, filters):
    return _get(txt, start, page_len)


def _get(text=None,start=0, page_len=5):
    return frappe.db.sql("""select DISTINCT t1.name, t1.employee_name from
            tabEmployee t1 where t1.status != "left" and (t1.name LIKE '%{text}%' or t1.employee_name LIKE '%{text}%') 
            ORDER  BY t1. employee_name limit {skip}, {limit} """.format(text=text, skip=start, limit=page_len))



@frappe.whitelist()
def get_directors(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""
		select u.name, concat(u.first_name, ' ', u.last_name)
		from tabUser u, `tabHas Role` r
		where u.name = r.parent and r.role = 'Directors' 
		and u.enabled = 1 and u.name like %s
	""", ("%" + txt + "%"))

@frappe.whitelist()
def get_approver_authorizer(emp):
    # first who the employee reports to
    # and up the ladder
    data = frappe.db.sql(""" SELECT c.reports_to approver, IFNULL(p.reports_to, c.reports_to) authorizer  from
          tabEmployee c JOIN tabEmployee p  ON (c.reports_to = p.name) WHERE c.name="{0}" """.format(emp), as_dict=1)
    d = []
    for datum in data:
        approver_name = frappe.get_value("Employee", datum.approver,"employee_name")
        authorizer_name = frappe.get_value("Employee", datum.authorizer,"employee_name")

        d= [{
            "approver":datum.approver,
            "authorizer":datum.authorizer,
            "approver_name":approver_name,
            "authorizer_name":authorizer_name
        }]

    return  d




def confirmation_notification():
    # get the list of employees that should be confirmed today
    # make sure it has not be confirmed
    # send bulk alert to all hr members
    import datetime
    from frappe import sendmail
    confirmees = frappe.get_list(doctype='Employee', filters=dict(final_confirmation_date=datetime.date.today()),
                                 fields=['employee_name', 'final_confirmation_date', 'date_of_joining'])

    message = "<div><ul style='list-style=none; margin:0; padding:0'>"
    for confirmee in confirmees:
        message += "<li style=><b>{employee_name}</b> employeed on {date_of_joining} is due for confirmation today ({final_confirmation_date}) </li>".format(
            **confirmee)

    message += "</ul><h3>Please attend to this ASAP.</h3></div>"

    if confirmees:
        # get all HR Users
        print message
        hr_users = frappe.db.sql("""select u.name from tabUser u, `tabHas Role` r where u.name = r.parent and 
			  r.role = 'HR User'and u.enabled = 1""", as_list=1)

        hr_users = [x[0] for x in hr_users]
        #hr_users = ["sylvester.amanyi@graceco.com.ng"]
        sendmail(recipients=hr_users, sender="erp@graceco.com.ng", subject=_("Employee Confirmation Notification"),
                 message=message,reply_to="erp@graceco.com.ng")



@frappe.whitelist()
def resolve_production_order(doctype, docname):
    # update without checking permissions
    frappe.db.sql("update `tab%s` set status = 'Resolved', skip_transfer=1 where name = '%s'" % (doctype, docname))
    return True