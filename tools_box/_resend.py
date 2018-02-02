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


def add_desktop():
    # get all admin icons
    # get all users
    # use admin icons to create icons for other user
    all_user = frappe.db.sql("select name from `tabUser` where enabled = 1 "
                             "and name != 'Administrator'", as_list=1)
    icons = frappe.get_all("Desktop Icon", {'owner': "Administrator"}, ["*"])
    for user in all_user:
        for icon in icons:
            icon = dict(icon)
            new_icon = frappe.new_doc("Desktop Icon")
            new_icon.owner = user[0]
            new_icon.color = icon.get('color')
            new_icon.app = icon.get('app')
            new_icon.idx = icon.get('idx')
            new_icon.blocked = icon.get('blocked')
            new_icon.label = icon.get('label')
            new_icon.force_show = 1
            new_icon.custom = icon.get('custom')
            new_icon.standard = icon.get('standard')
            new_icon.link = icon.get('link')
            new_icon.icon = icon.get('icon')
            new_icon.reverse = icon.get('reverse')
            new_icon.module_name = icon.get('module_name')
            new_icon._report = icon.get('_report')
            new_icon._doctype = icon.get('_doctype')
            new_icon.db_insert()
        break


from frappe.utils import flt, cint, cstr


def check_credit_limit():
    customer = "Adewunmi Abosede"
    company = "Graceco Limited"
    customer_outstanding = get_customer_outstanding(customer, company)
    frappe.errprint(customer_outstanding)


def get_customer_outstanding(customer, company):
    # Outstanding based on GL Entries
    outstanding_based_on_gle = frappe.db.sql("""select sum(debit) - sum(credit)
        from `tabGL Entry` where party_type = 'Customer' and party = %s and company=%s""", (customer, company))

    outstanding_based_on_gle = flt(outstanding_based_on_gle[0][0]) if outstanding_based_on_gle else 0
    frappe.errprint(outstanding_based_on_gle)

    # Outstanding based on Sales Order
    outstanding_based_on_so = frappe.db.sql("""
		select sum(base_grand_total*(100 - per_billed)/100)
		from `tabSales Order`
		where customer=%s and docstatus = 1 and company=%s
		and per_billed < 100 and status != 'Closed'""", (customer, company))

    outstanding_based_on_so = flt(outstanding_based_on_so[0][0]) if outstanding_based_on_so else 0.0

    # Outstanding based on Delivery Note
    unmarked_delivery_note_items = frappe.db.sql("""select
			dn_item.name, dn_item.amount, dn.base_net_total, dn.base_grand_total
		from `tabDelivery Note` dn, `tabDelivery Note Item` dn_item
		where
			dn.name = dn_item.parent
			and dn.customer=%s and dn.company=%s
			and dn.docstatus = 1 and dn.status not in ('Closed', 'Stopped')
			and ifnull(dn_item.against_sales_order, '') = ''
			and ifnull(dn_item.against_sales_invoice, '') = ''""", (customer, company), as_dict=True)

    outstanding_based_on_dn = 0.0

    for dn_item in unmarked_delivery_note_items:
        si_amount = frappe.db.sql("""select sum(amount)
			from `tabSales Invoice Item`
			where dn_detail = %s and docstatus = 1""", dn_item.name)[0][0]

        if flt(dn_item.amount) > flt(si_amount) and dn_item.base_net_total:
            outstanding_based_on_dn += ((flt(dn_item.amount) - flt(si_amount)) \
                                        / dn_item.base_net_total) * dn_item.base_grand_total

    frappe.errprint(outstanding_based_on_dn)
    frappe.errprint(outstanding_based_on_so)
    return outstanding_based_on_gle + outstanding_based_on_so + outstanding_based_on_dn
