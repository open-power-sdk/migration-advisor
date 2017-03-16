
#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2016 IBM Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

    Contributors:
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""
import unittest
from ma.xml_loader.quickfix_loader import QuickfixLoader


class QuickfixLoaderTest(unittest.TestCase):
    """ Test cases for the quickfix loader"""

    def get_include_test(self):
        """This test aim to check correct include value return from
        get_include() method in QuickfixLoader class"""
        quickfix_loader = QuickfixLoader()
        self.assertTrue(quickfix_loader.get_include('__bid128_inf') == 'math.h')
        self.assertTrue(quickfix_loader.get_include('__bid64_exp2') == 'math.h')
        self.assertTrue(quickfix_loader.get_include('__bid32_to_uint16_xint') == '')

    def get_type_test(self):
        '''This test aim to check correct replace return from
        get_type() method in QuickfixLoader class'''
        quickfix_loader = QuickfixLoader()
        self.assertTrue(quickfix_loader.get_type('__bid64_sub') == 'operator')
        self.assertTrue(quickfix_loader.get_type('__bid64dq_div') == 'operator')
        self.assertTrue(quickfix_loader.get_type('__bid32_log') == 'function')

    def get_value_test(self):
        """This test aim to check correct value return from
        get_value() method in QuickfixLoader class"""
        quickfix_loader = QuickfixLoader()
        self.assertTrue(quickfix_loader.get_value('__bid64_sub') == "-")
        self.assertTrue(quickfix_loader.get_value('__bid64qd_div') == '/')
        self.assertTrue(quickfix_loader.get_value('__bid64_mul') == '*')

    def get_define_test(self):
        """This test aim to check correct define value return from
        get_define() method in QuickfixLoader class"""
        quickfix_loader = QuickfixLoader()
        self.assertTrue(quickfix_loader.get_define('__bid32_ldexp') == '__STDC_WANT_DEC_FP__')
        self.assertTrue(quickfix_loader.get_define('__bid32_minnum_mag') == '__STDC_WANT_DEC_FP__')
        self.assertTrue(quickfix_loader.get_define('__bid32_from_int64') == '')
