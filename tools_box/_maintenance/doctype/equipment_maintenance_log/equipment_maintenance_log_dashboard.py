from frappe import _

def get_data():
	return {
		'fieldname': 'equipment_maintenance_log',
		'transactions': [
			{
				'label': _('Transactions'),
				'items': ['Job Card']
			},
		]
	}