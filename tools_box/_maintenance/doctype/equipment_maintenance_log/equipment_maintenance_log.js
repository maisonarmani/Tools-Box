// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

var DaysBetween = function (date1, date2) {
    //Get 1 day in milliseconds
    var one_day = 1000 * 60 * 60 * 24;
    // try reconverting to real date
    if (!(date1 instanceof Date)) {
        date1 = new Date(date1.replace(" ", "T"));
        date2 = new Date(date2.replace(" ", "T"));
    }
    // Convert both dates to milliseconds
    var date1_ms = date1.getTime();
    var date2_ms = date2.getTime();

    // Calculate the difference in milliseconds
    var difference_ms = date2_ms - date1_ms;
    //take out milliseconds
    difference_ms = difference_ms / 1000;
    //var seconds = Math.floor(difference_ms % 60);
    difference_ms = difference_ms / 60;
    var minutes = Math.floor(difference_ms % 60);
    difference_ms = difference_ms / 60;
    var hours = Math.floor(difference_ms % 24);
    var days = Math.floor(difference_ms / 24);


    return days + ' day(s), ' + hours + ' hour(s) and ' + minutes + ' minute(s)';
};


var get_employees = function () {
    return {
        query: "tools_box.controllers.api.get_active_employees"
    };
}
frappe.ui.form.on('Equipment Maintenance Log', {
    onload: function (frm,doc, docname) {
        frm.cscript.set_bd_time(doc,docname);
		frm.set_query("performed_by", get_employees);
    },
    refresh: function (frm) {
        var item_grouper =  function(p){ return { filters:{ asset_category : p } } };
        frm.fields_dict.equipment.get_query = item_grouper("Plant and Machinery");
    },
    start_time:function(frm,doc,docname){
        var end_time = frappe.model.get_value(doc,docname,"end_time");
        if(end_time != "") frm.cscript.set_bd_time(doc,docname);
    },
    end_time:function(frm,doc,docname){
        var start_time = frappe.model.get_value(doc,docname,"start_time");
        if(start_time != "") frm.cscript.set_bd_time(doc,docname);
    },
});

cur_frm.cscript.set_bd_time = function(doc,docname){
    var start_time = frappe.model.get_value(doc,docname,"start_time");
    var end_time = frappe.model.get_value(doc,docname,"end_time");
    if (start_time, end_time){
        frappe.model.set_value(doc,docname,"bd_time", DaysBetween(start_time, end_time));
    }

};

