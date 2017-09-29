
// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
var take = function(obj,param){
	var __self__ = this;
	if(typeof param !== 'string'){
		param.forEach(function(val){
			__self__[val] = obj[val] || "";
		});
	}else{
		__self__[param] = obj[param] || "";
	}
};

frappe.ui.form.on('Store Bin Card', {
    refresh: function(frm) {
        cur_frm.add_fetch("item_code","stock_uom","uom");
        cur_frm.add_fetch("item_code","item_name","item_name");
        cur_frm.add_fetch("item_code","description","description");
    },
    validate:function(frm) {
        if (frm.doc.action == "Receipt") {
            frm.doc.issue_item=[];
            validated = true;
            $.each(frm.doc.receipt_item,function(i,d){
                if (d.ref_doc!="Opening Stock" && (!d.ref_no || d.ref_no=="")) {
                    msgprint("Please enter the Reference No except for the Opening Stock");
                    validated=false;
                };
            });
            
        }else{
            frm.doc.receipt_item=[];
            validated = true;
        }
    }
});

var collected_items = [];
frappe.ui.form.on('Store Bin Card Issue Item', {
    ref_no:function(frm,doctype,docname) {
        var cur_doc = frappe.model.get_doc(doctype,docname);
        frappe.call({
            method: "tools_box._stock.doctype.store_bin_card.store_bin_card.get_items",
            args: {
                doctype: cur_doc.ref_doc,
                docname: cur_doc.ref_no
            },
            callback: function (ret) {
                if (ret != {}) {
                    var message = ret.message;
		            if (collected_items.findIndex((d)=> { return d == { a:cur_frm.doc.action, b:message[0].item_code } }) >= 0){
                        return;
                    }else{
                        collected_items.push({ a:cur_frm.doc.action,  b:message[0].item_code })
                    }
                    message.forEach(function (val) {
                        var d = frappe.model.add_child(cur_frm.doc, "Store Bin Card Issue Item", "issue_item");
                        take.apply(d, [val, [
                            'item_code', 'qty','item_name', 'uom','description'
                        ]]);
                        d.ref_doc = cur_doc.ref_doc;
                        d.ref_no = cur_doc.ref_no;
                    });

                    refresh_field('issue_item');
                }
            }

        });
    }
});

frappe.ui.form.on('Store Bin Card Item', {
    ref_no:function(frm,doctype,docname) {
        var cur_doc = frappe.model.get_doc(doctype,docname);
        frappe.call({
            method: "tools_box._stock.doctype.store_bin_card.store_bin_card.get_items",
            args: {
                doctype: cur_doc.ref_doc,
                docname: cur_doc.ref_no
            },
            callback: function (ret) {
                if (ret != {}) {
                    var message = ret.message;
		            if (collected_items.findIndex((d)=> { return d == message[0].item_code }) >= 0){
                        return;
                    }else{
                        collected_items.push(message[0].item_code)
                    }
                    message.forEach(function (val) {
                        var d = frappe.model.add_child(cur_frm.doc, "Store Bin Card Item", "receipt_item");
                        take.apply(d, [val, [
                            'item_code', 'qty','item_name', 'uom','description'
                        ]]);
                        d.ref_doc = cur_doc.ref_doc;
                        d.ref_no = cur_doc.ref_no;
                    });

                    refresh_field('receipt_item');
                }
            }
        });
    }
});


