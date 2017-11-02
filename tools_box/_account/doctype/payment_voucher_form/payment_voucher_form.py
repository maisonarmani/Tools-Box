# -*- coding: utf-8 -*-
# Copyright (c) 2015, bobzz.zone@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
class PaymentVoucherForm(Document):
	pass



@frappe.whitelist()
def make_payment_voucher_form(docname, doctype):
    document = frappe.get_doc(doctype, docname)

    pv = frappe.new_doc("Payment Voucher Form")

    pv.append("items", {

    })

    return pv.as_dict()