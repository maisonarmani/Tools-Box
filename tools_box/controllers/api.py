# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def get_active_employees(doctype, txt, searchfield, start, page_len, filters):
    return _get(txt, start, page_len)


def _get(text=None,start=0, page_len=5):
    return frappe.db.sql("""select DISTINCT t1.name, t1.employee_name from
            tabEmployee t1 where t1.status != "left" and (t1.name LIKE '%{text}%' or t1.employee_name LIKE '%{text}%') 
            ORDER  BY t1.employee_name limit {skip}, {limit} """.format(text=text, skip=start, limit=page_len))



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
