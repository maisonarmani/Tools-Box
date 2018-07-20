# -*- coding: utf-8 -*-
# Copyright (c) 2018, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class EmployeeRole(Document):
    def autoname(self):
        self.name = "{1}-{0}".format(self.department, self.designation)


@frappe.whitelist(True)
def get_timesheet_values(employee, from_date, to_date):
    # select timesheet details from timesheet where
    # must be submitted
    timesheet = frappe.db.sql("SELECT c.assessment_area, (SUM(c.self_score)/COUNT(c.self_score)) self_score, SUM(c.target_achieved) target_achieved, "
                              "SUM(c.target) target FROM `tabTimesheet` p INNER JOIN `tabTimesheet Detail` c "
                          "ON(c.parent = p.name) WHERE p.employee='{0}' AND  p.start_date >= DATE('{1}') AND "
                          "p.end_date <= DATE('{2}') GROUP BY c.assessment_area".format(employee, from_date ,to_date), as_dict=1)

    return timesheet

@frappe.whitelist(True)
def get_todo(department=None, designation=None,employee=None):
    # get the employee designation
    # based on the designation get the employee role
    # mapping the employee role, get the assessment area,
    # use the assessment information to get what should go where
    # and then send what goes to the timesheet to the timesheet
    # then send the details to the timesheet

    if designation or department:
        roles = get_employee_role(designation, department, 0)
        return roles
    else:
        employee = get_employee(employee)
        if employee:
            roles = get_employee_role(employee.designation, employee.department)
            return roles
    return None


def get_employee_role(designation, department, allow_timesheet=1):
    t = d = ""
    if allow_timesheet:
        t = " AND c.allow_timesheet = 1"

    if designation:
        d = " AND p.designation = '{0}'".format(designation)


    roles = frappe.db.sql(
        "SELECT DISTINCT  p.name, c.activity_type, c.target, c.assessment_area, c.has_target, c.target_frequency FROM `tabEmployee Role` as p "
        "INNER JOIN `tabEmployee Role Item` as c"
        " ON(p.name= c.parent) WHERE (p.department ='{1}' {2} {0}) AND target_frequency='Daily'"
            .format(d, department, t), as_dict=1)

    return roles


def get_employee(employee):
    employee = frappe.get_list(doctype="Employee", fields=["name", "department", "designation"],
                               filters={'name': employee})

    if employee:
        return employee[0]
    return None
