# -*- coding: utf-8 -*-
# Copyright (c) 2018, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class EmployeeRole(Document):
    def autoname(self):
        self.name = "{1}-{0}".format(self.department, self.designation)


@frappe.whitelist(False)
def get_todo():
    # get the employee designation
    # based on the designation get the employee role
    # mapping the employee role, get the assessment area,
    # use the assessment information to get what should go where
    # and then send what goes to the timesheet to the timesheet
    # then send the details to the timesheet
    
    department = designation = ""

    if designation or department:
        roles = get_employee_role(designation, department, 0)
        return roles
    else:
        employee = get_employee(frappe.session.data.user)
        if employee:
            roles = get_employee_role(employee.designation, employee.department)
            return roles
    return None


def get_employee_role(designation, department, allow_timesheet=1):
    if allow_timesheet:
        allow_timesheet = " AND c.allow_timesheet = 1"

    roles = frappe.db.sql(
        "SELECT DISTINCT  p.name, c.activity_type, c.target, c.has_target, c.target_freqency FROM `tabEmployee Role` as p "
        "INNER JOIN `tabEmployee Role Item` as c"
        " ON(p.name= c.parent) WHERE (p.department ='{1}' {2}) OR p.designation = '{0}'"
            .format(designation, department, allow_timesheet), as_dict=1)

    return roles


def get_employee(user):
    employee = frappe.get_list(doctype="Employee", fields=["name", "department", "designation"],
                               filters={"user_id": user})

    if employee:
        return employee[0]
    return None
