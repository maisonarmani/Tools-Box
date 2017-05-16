frappe.listview_settings['Fire Extinguisher'] = {
	add_fields: ["status"],
	get_indicator: function(doc) {
        return [__(doc.status),{
            'Fault':'red',
            'Empty':'red',
            'No Action':'green',
            'Remedial':'black',
            'No Fault':'green'
        }[doc.status],"status,=," + doc.status];
	}
};
