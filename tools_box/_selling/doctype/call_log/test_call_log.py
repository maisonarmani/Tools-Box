# -*- coding: utf-8 -*-
# Copyright (c) 2015, bobzz.zone@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals
from frappe import db
import frappe
import unittest


# test_records = frappe.get_test_records('Call Log')

class TestCallLog(unittest.TestCase):
    pass


def run_test():
    #

    ''''# create user
    user = "lara@gmail.com"
    doc = frappe.get_doc({
        "full_name":"Maison Armani",
        "first_name":"Maison",
        "last_name":"Armani",
        "username":"lara",
        "email": user,
        "doctype": "User",
        "enabled":1
    })
    doc.add_roles("File User")
    doc.db_update()
    '''

    parent = ""
    folders = []
    root = "Home"
    client_name = "Barcelona"
    client_structure = {
        client_name: {
            "Folder 1": "Folder 1",
            "Folder 2": "Folder 2",
            "Folder 3": "Folder 3",
            "Folder 4": ["Sub Folder 1"]
        }
    }

    for (key, client) in client_structure.items():
        if parent is "":
            parent = _p = "{0}".format(root)
            folders.append({"parent": parent, "folder_name": key})
        if isinstance(client, dict):
            for (k, v) in client.items():
                parent = "{0}/{1}".format(_p, key)
                folders.append({"parent": parent, "folder_name": k})
                if isinstance(v, list):
                    for i in v:
                        folders.append({"parent": "{0}/{1}".format(parent, k), "folder_name": i})

    client_user_role = client_name + " - User"
    client_admin_role = client_name + " - Admin"
    if folders:
        create_new_role(client_user_role)
        create_new_role(client_admin_role)


    for folder in folders:
        # create user and pass admin
        create_new_folder(folder.get('folder_name'), folder.get('parent'), client_user_role, client_admin_role)


def create_new_folder(file_name, folder, user, admin):
    file = frappe.new_doc("File")
    file.file_name = file_name
    file.is_folder = 1
    file.folder = folder
    file.file_user = user
    file.file_admin = admin
    file.insert()


def create_new_role(role):
    l = frappe.get_doc({
        "role_name": role,
        "doctype": "Role",
        "desk_access": 1
    })
    l.insert()



def get_permission_query_conditions_for_file(user):
    roles = ','.join([str("\"" + i + "\"") for i in frappe.get_roles(user)])
    roled = "select tabFile.name from tabFile where (tabFile.file_user in ({roles}) or tabFile.file_admin in ({roles}))"
    if "System Manager" in frappe.get_roles(user):
        return None
    elif "File User" in frappe.get_roles(user):
        return """(tabFile.owner = '{user}') or ((tabFile.is_folder = 0) and tabFile.folder in ({roled})) or
        (tabFile.name in ({roled}))""".format(user=frappe.db.escape(user), roled=roled.format(roles=roles))


def get_base_files():
    user = user = "mercy.jimah@graceco.com.ng"
    data= db.sql("select file_name, file_url, old_parent from `tabFile` where ({}) and (old_parent = '{base}')"
                 .format(get_permission_query_conditions_for_file(user), base="Home"), as_dict= 1)
    print data

