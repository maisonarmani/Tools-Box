# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
from frappe.core.doctype.file.file import create_new_folder, FolderNotEmpty

import frappe


@frappe.whitelist()
def change_owner(doctype=None, docname=None, new_owner=None):
    if doctype and docname and new_owner:
        frappe.db.sql("update `tab{}` set file_user=\"{}\" where name like \"{}\"".format(doctype, new_owner, docname))


@frappe.whitelist()
def make_private(doctype=None, docname=None):
    public_private(doctype, docname)


@frappe.whitelist()
def make_public(doctype=None, docname=None):
    role = frappe.db.sql("select file_admin from `tab{}` where name = \"{}\"".format(doctype, docname))[0][0]
    role = str(role).replace("Admin", "User")
    public_private(doctype, docname, role)


def public_private(doctype=None, docname=None, role=None):
    if doctype and docname:
        frappe.db.sql("update `tab{}` set file_user=\"{}\" where name like \"{}%\"".format(doctype, role, docname))
