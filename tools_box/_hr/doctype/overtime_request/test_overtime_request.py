# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
from tools_box.controllers.api import confirmation_notification

class TestOvertimeRequest(unittest.TestCase):
	pass


def get_notification():
	confirmation_notification()