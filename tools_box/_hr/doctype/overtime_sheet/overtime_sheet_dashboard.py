from frappe import _

def get_data():
	return {
		'fieldname': 'overtime',
		'transactions': [
			{
				'label': _('Transactions'),
				'items': ['Expense Claim']
			},
		]
	}