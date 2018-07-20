from frappe import _

def get_data():
	return {
		'heatmap': False,
		'transactions': [
			{
				'label': _(''),
				'items': ['Stock Entry']
			},
		]
	}