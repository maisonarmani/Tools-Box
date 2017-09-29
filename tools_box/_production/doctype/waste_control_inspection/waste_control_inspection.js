// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
var take = function(obj,param){
	var __self__ = this;
	if(typeof param !== 'string'){
		param.forEach(function(val){
			__self__[val] = obj[val];
		});
	}else{
		__self__[param] = obj[param];
	}
};
frappe.ui.form.on('Waste Control Inspection', {
	refresh: function(frm) {
		console.log(frm.doc.__last_sync_on)
		if (frm.doc.__last_sync_on == undefined){
			var activities = [
				{activity:"Are the available wastes evacuated?"},
				{activity:"Is there any abandoned wrapper?"},
				{activity:"Are the waste bins around emptied?"},
				{activity:"Is there any damaged faucet?"},
				{activity:"Are packaged products weights okay?"},
				{activity:"Are Personal Protective Equipment (PPE) used by Staff Members on the Floors? "},
				{activity:"Are mixing, kneading, depositing and packaging machines cleaned and effective?"},
				{activity:"Has the daily production output report for waste minimization control sheet been checked and filled? "},
				{activity:"Has the daily wrapper waste monitoring control sheets been checked?"},
				{activity:"Has the packaging downtime forms been checked?"},
				{activity:"Have the workers been orientated on how to handle raw materials, unfinished products and finished products?"},
				{activity:"Are paper cups appropriate for use?"},
				{activity:"Are the ovens used functioning properly?"},
				{activity:"Is the condition for cooled cupcakes okay?"},
				{activity:"Are the packaging machines generating waste?"},
				{activity:"Is frying machine in good working condition?"},
				{activity:"Are the weighing scales okay?"},
				{activity:"Are the packaging machines generating waste?"},
				{activity:"Is there any saleable waste material available?"},
				{activity:"Are the available waste materials sorted, arranged and counted?"},
				{activity:"Is there any observation?"},
			]
			activities.forEach(function(val){
				var d = frappe.model.add_child(frm.doc, "Waste Control Inspection Items", "activities");
				take.apply(d,[val,[
					'activity'
				]]);
				d.completed = "No";
				d.corrective_action = "";
				d.commen = "";
			});

			refresh_field('activities')
		}

	}
});
