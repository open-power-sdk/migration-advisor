# -*- coding: utf-8 -*-
"""
Copyright (C) 2016 IBM Corporation

Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

    Contributors:
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""

import xml.etree.ElementTree as elemTree
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
QUICKFIX_XML = DIR_PATH + "/../resources/api_dfp_quickfix.xml"


class QuickfixLoader(object):
    """Class to load Quickfix Loader for MA.
    This class get information stored in XML file
    into a python module"""
    def __init__(self):
        self.items = {}
        self.load_xml(QUICKFIX_XML)

    def load_xml(self, file_name):
        '''Method to load Quickfixes strings.
        This method open XML file and load info inside a
        dictionary data structure'''

        tree = elemTree.parse(file_name)
        root = tree.getroot()
        orig_item = None

        for item in root.iter():
            if item.tag == 'item':
                orig_item = item.attrib

            if item.tag == 'replacer':
                replacer = item.attrib
                self.items[orig_item['target']] = [orig_item, replacer]

    def get_include(self, target):
        '''Method to get include value for selected target'''
        replacer = self.items[target][1]
        return replacer['include']

    def get_type(self, target):
        '''Method to get type value for selected target'''
        replacer = self.items[target][1]
        return replacer['type']

    def get_value(self, target):
        '''Method to get type value for selected target'''
        replacer = self.items[target][1]
        return replacer['value']

    def get_define(self, target):
        '''Method to get define value for selected target'''
        replacer = self.items[target][1]
        return replacer['define']
