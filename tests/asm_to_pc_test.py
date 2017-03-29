#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2017 IBM Corporation

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
from ma.xml_loader.asm_to_ppc import AssemblyReplacer


class AssemblyReplacerTest(unittest.TestCase):
    """ Test cases for the Assembly replacer """

    def get_replace_test(self):
        '''This test aim to check correct replace value return from
        get_replace() method in AssemblyReplacer class'''
        asm_replacer = AssemblyReplacer()
        self.assertTrue(asm_replacer.get_replace('lock;xchgl;') ==
                        "__atomic_test_and_set(/*void *ptr, int memmodel*/);")
        self.assertTrue(asm_replacer.get_replace('lock;orl;') ==
                        "__atomic_fetch_or(/*type *ptr, type val, int memmodel*/);")
        self.assertTrue(asm_replacer.get_replace('pause;') == "\"or 27,27,27; isync\"")

    def get_type_test(self):
        '''This test aim to check correct type return from
        get_type() method in AssemblyReplacer class'''
        asm_replacer = AssemblyReplacer()
        self.assertTrue(asm_replacer.get_type('lock;xchgl;') == "builtin")
        self.assertTrue(asm_replacer.get_type('lock;orl;') == "builtin")
        self.assertTrue(asm_replacer.get_type('rdtsc;') == "asm")
        self.assertTrue(asm_replacer.get_type('pause;') == "asm")
