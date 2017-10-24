from frappe import _

def get_data():
	return {
		'fieldname': 'purchase_requisition',
		'transactions': [
			{
				'label': _('Transactions'),
				'items': ['Purchase Order']
			},
		]
	}