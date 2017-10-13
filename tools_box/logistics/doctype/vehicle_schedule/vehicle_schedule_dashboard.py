from frappe import _

def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on transactions against this Vehicle Schedule. See timeline below for details'),

		'fieldname': 'vehicle_schedule',
		'transactions': [
			{
				'label': _('Transactions'),
				'items': ['Purchase Order']
			},
		]
	}