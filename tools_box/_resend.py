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


def stock_reconciliation():
    # read the excel file
    # use the record to create actual stock recon
    # check to make sure it actually does that
    from  openpyxl import load_workbook
    from openpyxl import cell
    wb = load_workbook(filename="/home/frappe/ma.xlsx")
    sheet_names = wb.get_sheet_names()

    # get all header
    for headers in wb[sheet_names[0]]:
        for header in headers:
            # header = cell.Cell(header)
            print header.coordinate

        del headers
        break


def add_logo():
    fr = frappe.db.sql("select name, message from `tabEmail Alert`", as_dict=1)
    for f in fr:
        new_message = """
						<img src="http://41.79.117.124/files/GC_0313-GraceCo logo-v2.jpg" style="float: right;"><div><div><b>Graceco Limited</b></div>
						<div>5-9 Temitayo Street</div><div>Off Nureni Yusuff Road</div><div>Kollington, Alagbado</div>
						<div>Lagos State</div><div>Tel: +234 8093931020</div><div><b>email:</b> sales@graceco.com.ng</div>
						<div><b>web: </b><a href="http://www.graceco.com.ng" rel="nofollow">www.graceco.com.ng</a></div>
						</div>
						<!---main content-->
						<div>%s</div>""" % f.message

        frappe.db.sql("update `tabEmail Alert` set message = '%s' where name='%s'" % (new_message, f.name))
