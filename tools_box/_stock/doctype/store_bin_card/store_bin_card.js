
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