// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Equipment Maintenance Log', {
    onload: function (frm) {
        console.log("Loading...");
    },
    refresh: function (frm) {
        var item_grouper =  function(p){ return { filters:{ item_group : p } } };
        frm.fields_dict.equipment.get_query = item_grouper("Fixed Assets");
        frm.fields_dict.spare_parts_used.get_query = item_grouper("Spares Parts");
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
    var end_time = frappe.model.get_value(doc,docname,"start_time");
    var start_time = frappe.model.get_value(doc,docname,"end_time");
    frappe.model.set_value(doc,docname,"bd_time",moment(start_time).diff(end_time,"days"));
};

