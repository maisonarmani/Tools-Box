from frappe import _

def get_data():
	return {
		'fieldname': 'overtime_request',
		'transactions': [
			{
				'label': _('Transactions'),
				'items': ['Overtime Sheet']
			},
		]
	}