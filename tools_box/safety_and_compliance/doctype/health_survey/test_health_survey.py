# -*- coding: utf-8 -*-
# Copyright (c) 2015, masonarmani38@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
import redis
from frappe import conf
# test_records = frappe.get_test_records('Health Survey')

END_LINE = '<!-- frappe: end-file -->'
TASK_LOG_MAX_AGE = 86400  # 1 day in seconds
redis_server = None

class TestHealthSurvey(unittest.TestCase):
	def test_redis(self):
		print (type(frappe.as_json({'event': 'test', 'message': {'test':'Test Data'}, 'room': get_site_room()})))
		r = get_redis_server()
		try:
			r.publish('events', frappe.as_json({'event': 'test', 'message': {'test':'Test Data'}, 'room': get_site_room()}))
		except redis.exceptions.ConnectionError:
			print(frappe.get_traceback())
			pass


def get_redis_server():
	"""returns redis_socketio connection."""
	global redis_server
	if not redis_server:
		from redis import Redis
		redis_server = Redis.from_url(conf.get("redis_socketio")
			or "redis://localhost:12311")
	return redis_server


def get_doc_room(doctype, docname):
	return ''.join([frappe.local.site, ':doc:', doctype, '/', docname])

def get_user_room(user):
	return ''.join([frappe.local.site, ':user:', user])

def get_site_room():
	return ''.join([frappe.local.site, ':all'])

def get_task_progress_room(task_id):
	return "".join([frappe.local.site, ":task_progress:", task_id])
