import frappe
from frappe.email.doctype.email_queue.email_queue import retry_sending


def resend():
    data = []
    data = frappe.db.sql(
        'select name from `tabEmail Queue` where status = "error" and creation >= DATE("2017-05-30") limit 40',
        as_list=1)
    for datum in data:
        retry_sending(datum[0])
    print data


def set_employee():
    employee = frappe.get_doc("Employee", "GCL-EMP/0882")
    employee.user_id = "Administrator"
    employee.save(ignore_permissions=True)



def add_cf():
    file = frappe.db.sql("select name from `tabFile` where name = '{0}'".format("Home/Case Files"), as_dict=1)
    if len(file) == 0:
        create_new_folder("Case Files", "Home")
    create_new_folder("Matter 01-01-01", "Home/Case Files")


def create_new_folder(file_name, folder=None):
    file = frappe.new_doc("File")
    file.is_home_folder = 1
    file.file_name = file_name
    file.is_folder = 1
    file.folder = folder
    file.insert()



def update_shared():
    import frappe.share
    # every user must have access to his / her own detail
    employees = frappe.get_all("Employee", filters={"status": "Active"})
    emps = [emp.name for emp in employees]
    users = [emp.user_id for emp in employees]

    for index, user in enumerate(users):
        frappe.share.add("Employee", emps[index], user, read=1, share=1)

