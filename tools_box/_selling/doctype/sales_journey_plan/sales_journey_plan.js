// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

var DMAP = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5
};

frappe.ui.form.on('Sales Journey Plan', {
    from: function () {
        cur_frm.trigger('prefill')

    },
    prefill: function (frm, doctype, docname) {
        if (frm.doc.from != undefined) {
            frappe.model.set_value(doctype, docname, "to", frappe.datetime.add_days(frm.doc.from, 6))
        }
        setDOTW(frm);
    }
});


var opts = {
    existing_outlets_add: function (frm, doctype, docname) {
        setPref(frm, doctype, docname)
    },
    new_outlets_add: function (frm, doctype, docname) {
        setPref(frm, doctype, docname)
    },
    existing_outlets_remove: function (frm) {
        sumRoutes(frm, frm.doctype, frm.docname)
    },
    new_outlets_remove: function (frm) {
        sumRoutes(frm, frm.doctype, frm.docname)
    },
    day_of_the_week: function (frm, doctype, docname) {
        setDOTW(frm, doctype, docname)
    }
}

frappe.ui.form.on('Sales Journey Plan New Item', opts);
frappe.ui.form.on('Sales Journey Plan Existing Item', opts);

var setPref = function (frm, doctype, docname) {
    var items = frappe.model.get_list(doctype);
    if (items.length > 1) {
        var last = items[items.length - 2]; // last is previous item
        frappe.model.set_value(doctype, docname, "date", last.date);
        frappe.model.set_value(doctype, docname, "day_of_the_week", last.day_of_the_week);
        frappe.model.set_value(doctype, docname, "territory", last.territory);
    }

    sumRoutes(frm, frm.doctype, frm.docname);
    setDOTW(frm, doctype, docname)
}

var setDOTW = function (frm, doctype, docname) {
    var dotw = frappe.model.get_value(doctype, docname, "day_of_the_week");
    var addition = frappe.datetime.add_days(frm.doc.from, DMAP[dotw]);
    frappe.model.set_value(doctype, docname, "date",addition);

    if (doctype == undefined) {
        if (frm.doc.existing_outlets) {
            frm.doc.existing_outlets.forEach(function (_) {
                setDOTW(frm, _.doctype, _.name)
            });
        }

        if (frm.doc.new_outlets) {
            frm.doc.new_outlets.forEach(function (_) {
                setDOTW(frm, _.doctype, _.name)
            })
        }
    }
}


var sumRoutes = function (frm, doct, docn) {
    frappe.model.set_value(doct, docn, "total_routes",
        frm.doc.existing_outlets ? frm.doc.existing_outlets.length : 0  +
        frm.doc.new_outlets ? frm.doc.new_outlets.length : 0 )
}