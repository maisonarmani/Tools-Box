// Copyright (c) 2016, bobzz.zone@gmail.com and contributors
// For license information, please see license.txt
frappe.ui.form.on('Payment Voucher Form', {
	refresh: function(frm) {
		cur_frm.set_query("bank_name", function() {
			return {
				"filters": [
					["Account","account_type","in","Bank,Cash"],
					["Account", "is_group","in","0"]
				]
			};
		});
		cur_frm.set_query("expense_account", function() {
			return {
				"filters": [
					["Account","is_group","=","0"],
					//["Account","rgt","<=","561"],
					["Account","root_type","=","Expense"]
				]
			};
		});
	}
});
