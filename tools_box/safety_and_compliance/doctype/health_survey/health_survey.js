// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

cur_frm.add_fetch('employee_id', 'department', 'employee_department');
cur_frm.add_fetch('employee_id', 'employee_name', 'employee_name');
cur_frm.add_fetch("employee_id", "current_address","background_information");

var get_employees = function () {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}

frappe.ui.form.on('Health Survey', {
	onload:function(frm,cdt,cdn){
		frm.set_query("employee_id", get_employees);
	},
	refresh: function(frm,cdt,cdn) {
		console.log(frm);
        if (frm.doc.reported_by == "" || frm.doc.reported_by == undefined) {
        	frappe.model.set_value(cdt, cdn, 'reported_by',user_fullname);
        }
	}
});

cur_frm.cscript.employee_id = function(doc){
	frappe.call({
		method:'tools_box.safety_and_compliance.api.get_employee',
		args:{
			employee_id:doc.employee_id,
			fields:'date_of_joining as doj'
		},
		callback:function(r){
			if(r.message.doj){
				var df = moment(frappe.datetime.get_today()).diff(r.message.doj,'months');
				if(df >= 12){
					df = [Math.floor(df / 12),df % 12];
					var year_desc = [df[0] , df[0] > 1 ? " years" :' year'].join(" ")
					var month_desc = [df[1] , df[1] > 1 ? " months" : ' month'].join(" ")
					var df_desc = [year_desc,month_desc].join(" and ");
				}
				else{
					var df_desc = [df , df > 1 ? " months" : ' month'].join(" ")
				}
				cur_frm.set_value('how_long_working',df_desc);
			}
		}
	});
};