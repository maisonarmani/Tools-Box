frappe.views.calendar["Job Card"] = {
	field_map: {
		"start": "job_card_date",
		"end": "proposed_completion_date",
		"id": "name",
		"title": "job_description",
		"status": "status",
	},
	get_events_method: "erpnext.support.doctype.job_card.job_card.get_job_cards"
}
