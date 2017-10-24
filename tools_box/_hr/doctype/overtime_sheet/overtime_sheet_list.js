// Copyright (c) 2017, masonarmani38@gmail.com and Contributors
// License: GNU General Public License v3. See license.txt

frappe.listview_settings['Overtime Sheet'] = {
    onload: function (doclist) {
        doclist.list_renderer.settings.setup_menu(doclist);
    },
    setup_menu: function (doclist) {
        doclist.page.add_menu_item(__("Process Expense Claim"), function () {
            var selected = doclist.get_checked_items() || [];
            if (selected.length <= 0) {
                frappe.throw("No overtime sheet was selected.")
            }
            var _docnames = ""
            selected.forEach(function(v){
                _docnames += "~~"+v._name
            })
            frappe.call({
                method: "tools_box._hr.doctype.overtime_sheet.overtime_sheet.make_expense_claim_from_list",
                args: {
                    docnames:_docnames
                },
                callback: function (r) {
                    frappe.model.sync(r.message);
                    frappe.set_route('Form', 'Expense Claim', r.message.name);
                }
            });
        })
    }
}