# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
    columns = [
        "ID:Link/Expense Claim:150",
        "Approval Status:Data:100",
        "Total Claimed Amount:Currency:150",
        "Total Sanctioned Amount:Currency:150",
        "Posting Date:Date:100",
        "From Employee:Link/Employee:100",
        "Employee Name:Data:170",
        "Company:Link/Company:100",
    ]
    data = []
    conditions, addition, add_columns = "", "", ""
    if filters.get('posting_from') and filters.get('posting_to'):
        conditions += ' and tabEC.posting_date  BETWEEN DATE(\'{0}\') and DATE(\'{1}\')' \
            .format(filters.get('posting_from'), filters.get('posting_to'))

    if filters.get("approval_status") and filters.get("approval_status") != "All":
        add_columns = ", c1.comment_by_fullname"
        addition = "LEFT OUTER JOIN tabComment c1 ON tabEC.name = c1.comment_docname and c1.comment = '{0}'"
        if filters.get("approval_status") == "Authorized":
            addition = addition.format("Authorized")
            columns += ["Authorized By:Data:170"]
        elif filters.get("approval_status") == "IAD Cleared":
            addition = addition.format("IAD Cleared")
            columns += ["IAD Cleared By:Data:170"]
        conditions += ' and tabEC.approval_status = \'{0}\''.format(filters.get('approval_status'))

    if filters.get("doc_status") and filters.get("doc_status") != "All":
        conditions += ' and tabEC.docstatus = {0}'.format(filters.get('doc_status'))

    sql = '''select tabEC.name , tabEC.approval_status, tabEC.total_claimed_amount, tabEC.total_sanctioned_amount,
              tabEC.posting_date, tabEC.employee,tabEC.employee_name,tabEC.company {add_columns} 
                from `tabExpense Claim`tabEC {addition} WHERE (1=1) {0} ORDER BY tabEC.name'''

    frappe.errprint(sql.format(conditions, addition=addition, add_columns=add_columns))
    data = frappe.db.sql(sql.format(conditions, addition=addition, add_columns=add_columns), as_list=1)
    return columns, data
