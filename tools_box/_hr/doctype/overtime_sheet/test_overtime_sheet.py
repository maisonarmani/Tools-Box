# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest


class TestOvertimesheet(unittest.TestCase):
	pass

def testCOA():
	default_income_account =frappe.get_value("Company", "Graceco Limited", "default_income_account")
	sub_accs = frappe.db.sql("select name from `tabAccount` where parent_account='Sales Income - GCL'", as_list=1)

	# get total of all the sales invoice gl entry
	s_accs = ()
	for sub_acc in sub_accs:
		s_accs += (str(sub_acc[0]),)

	# get difference
	sql1 = "SELECT SUM(credit) - SUM(debit) FROM `tabGL Entry` WHERE posting_date BETWEEN DATE('2017-01-01') AND DATE('2017-10-30')" \
		  " AND voucher_type = 'Sales Invoice' AND account IN {s}".format(s=str(s_accs))

	sql2 = "SELECT si.name , SUM(soi.amount), COUNT(soi.name) from `tabSales Invoice Item`  soi INNER JOIN " \
		   "`tabSales Invoice`  si ON(si.name =soi.parent) WHERE si.name IN(select voucher_no from `tabGL Entry` where " \
		   " voucher_type='Sales Invoice' and posting_date between date('2017-01-01') and date('2017-10-30')" \
		   " AND account IN {s}) AND si.docstatus=1 AND si.status != 'Return' GROUP BY si.name  LIMIT 20".format(s=str(s_accs))


	sql1_1 = "SELECT SUM(debit), voucher_no FROM `tabGL Entry` WHERE posting_date BETWEEN DATE('2017-01-01') AND DATE('2017-10-30')" \
		  " AND debit != 0 AND voucher_type = 'Sales Invoice' AND account IN {s} GROUP BY voucher_no LIMIT 20".format(s=str(s_accs))

	sql1_2 = "SELECT si.name, SUM(soi.net_amount),SUM(soi.amount)  from `tabSales Invoice Item`  soi INNER JOIN " \
		   "`tabSales Invoice`  si ON(si.name =soi.parent) WHERE si.name IN(select voucher_no from `tabGL Entry` where " \
		   " voucher_type='Sales Invoice' and posting_date between date('2017-01-01') and date('2017-10-30')" \
		   " AND account IN {s}) AND soi.net_amount != soi.amount AND si.docstatus=1 AND si.status = 'Return' GROUP BY si.name LIMIT 20 ".format(s=str(s_accs))

	# get count
	sql3 = "select count(DISTINCT voucher_no) from `tabGL Entry` where  voucher_type='Sales Invoice' and posting_date between date('2017-01-01') " \
		  "and date('2017-10-30') AND account IN {s}".format(s=str(s_accs))

	sql4 = "SELECT SUM(soi.net_amount)  from `tabSales Invoice`  si  JOIN `tabSales Invoice Item`  soi   ON(si.name =soi.parent) " \
		   "WHERE  si.posting_date between date('2017-01-01') AND date('2017-10-30') AND soi.income_account IN {s} ".format(s=str(s_accs))

	sql5 = "SELECT count(si.name)  from `tabSales Invoice`  si  WHERE  si.posting_date between date('2017-01-01') AND date('2017-10-30') "

	sql6 = "select voucher_no, count(voucher_no) from `tabGL Entry` where  voucher_type='Sales Invoice' and posting_date between date('2017-01-01') " \
		  "and date('2017-10-30') AND account IN {s} GROUP BY voucher_no HAVING COUNT(*) > 1".format(s=str(s_accs))

	print sql4
	print frappe.db.sql(sql4)