// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

const CMODULE = "tools_box.safety_and_compliance";

frappe.ui.form.on('Head Count', {
	onload:function(frm){

	},
	refresh: function(frm) {
//		cur_frm.cscript.get_previous_count_date();
	},
});

//
frappe.ui.form.on('Head Count Detail', {
	head_count_details_add: function(frm) {
		cur_frm.cscript.compute_total();
	},
	head_count_details_remove: function(frm) {
		cur_frm.cscript.compute_total();
	},
	head_count_details_move: function(frm) {
		cur_frm.cscript.compute_total();
	},
	head_count_details_beforeremove: function(frm) {
		console.log("Called before removing a grid item");
	},
	count:function(frm){
		cur_frm.cscript.compute_total();
	},
	staff:function(frm){
		frm.add_fetch("staff","employee_name","staff_name");
	}

});

var filters = {
	filter:{
		department:'Safety and Compliance'
	}
};
cur_frm.cscript.set_child_queries = function g(frm){
	// Staff is a field in the Head Count Table
	frm.doc['head_count_details'].grid.get_field("staff").get_query(function(doc) {
		return filters;
	});
};

// Set query filter for employee id
cur_frm.set_query("employee_id",function g(){
	return filters;
});

cur_frm.cscript.get_previous_count_date = function(){
	frappe.call({
		type:'GET',
		method:[CMODULE,"doctype.head_count.head_count.get_previous_date"].join("."),
		args:{
			current_date: cur_frm.doc.current_count_date
        },
		callback:function(){
			// do something
		}
	})
};
cur_frm.cscript.compute_total = function(){
	// loopthru the grid and get sum the values in the count field
	var sum = 0;
	cur_frm.doc.head_count_details.forEach(function(val){
		sum += val.count;
	});
	frappe.model.set_value(cur_frm.doctype,cur_frm.docname,"total_count",sum)
};

// fetches
cur_frm.add_fetch("employee_id","employee_name","staff_full_name");
