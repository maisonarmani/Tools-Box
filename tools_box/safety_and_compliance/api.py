# -*- coding: utf-8 -*-
# Copyright (c) 2015, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.desk.reportview import get_match_cond


@frappe.whitelist()
def employee_query(doctype, txt, searchfield, start, page_len, filters):
    if filters.get('status'):
        cond = "status = '{status}' and ".format(**filters)

    sql = """select name,employee_name from `tabEmployee` where (1=1) and ( {cond} {key} like %(txt)s) {mcond} 
        order by if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999), name limit %(start)s, %(page_len)s""" \
    .format(**{
        "cond": cond,
        'key': searchfield,
        'mcond': get_match_cond(doctype),
    }), {
              'txt': "%%%s%%" % txt,
              '_txt': txt.replace("%", ""),
              'start': start,
              'page_len': page_len
          }
    return frappe.db.sql(*sql)


@frappe.whitelist()
def get_employee(employee_id, fields=None):
    employee = []
    if employee_id:
        try:
            employee = frappe.db.get_all('Employee', fields=[fields], filters={'name': employee_id})
            employee = employee[0]
        except frappe.DoesNotExistError as err:
            frappe.throw(_("Employee not found"))
    return employee


@frappe.whitelist()
def get_employee_experience(employee_id):
    employee, experience = [], []
    if employee_id:
        employee = frappe.get_doc('Employee', employee_id)
        if employee:
            experience = {
                'internal': employee.internal_work_history,
                'external': employee.external_work_history
            }
    return experience


@frappe.whitelist()
def update_experience(employee_id):
    employee, experience = [], []
    if employee_id:
        employee = frappe.get_doc('Employee', employee_id)
        if employee:
            experience = {
                'internal': employee.internal_work_history,
                'external': employee.external_work_history
            }
    return experience


from frappe.model.mapper import get_mapped_doc
import inspect


@frappe.whitelist()
def map_test(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.ignore_pricing_rule = 1
        target.run_method("test_map")

    print(inspect.getargspec(get_mapped_doc))

    def update_item(source_doc, target_doc, source_parent):
        pass

    doc = get_mapped_doc("Fire Extinguisher Inspection", source_name, {
        "Fire Extinguisher Inspection": {
            "doctype": "Fire Extinguisher Inspection Car",
            "validation": {
                "docstatus": ["=", 0]
            },
            "field_map": {
                'name': 'created_from'
            },
            "add_if_empty": False,
            "postprocess": update_item,
            "condition": lambda doc: doc.docstatus == 1
        },
    }, target_doc, set_missing_values)

    return doc
