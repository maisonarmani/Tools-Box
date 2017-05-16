
import frappe
from frappe.jobs.background_jobs import enqueue

def long_job(arg1, arg2):
	'''Hi !!!'''
	frappe.publish_realtime('msgprint', 'Starting long job...')
	# this job takes a long time to process
	frappe.publish_realtime('msgprint', 'Ending long job...')

def enqueue_long_job(arg1, args2):
	'''Hi !!!'''
	enqueue('graceco_tools.safet.mymodule.long_job', arg1=arg1, arg2=arg2)