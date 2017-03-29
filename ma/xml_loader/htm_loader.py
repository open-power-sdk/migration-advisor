# -*- coding: utf-8 -*-
"""
Copyright (C) 2017 IBM Corporation

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
        * Daniel Kreling <dbkreling@br.ibm.com>
"""

import xml.etree.ElementTree as elemTree
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
HTM_FILE = DIR_PATH + "/../resources/htm.xml"


class HtmLoader(object):
    """ Load htm.xml information into a Python element"""

    def __init__(self):
        self.htms = []
        self.htms_include = []
        self.__load_xml(HTM_FILE)

    def __load_xml(self, file_name):
        """Load the contents of htm.xml into a Python element"""
        tree = elemTree.parse(file_name)
        self.root = tree.getroot()
        for htm in self.root.iter('function'):
            self.htms.append(htm.attrib)
        for htm_header in self.root.iter('header'):
            self.htms_include.append(htm_header.attrib)

    def get_functions(self):
        """Populate a list of HTM names"""
        for htm in self.root.findall('htmapi'):
            if htm.get("type") == "function":
                self.htms.append(htm.get('target'))
        return self.htms

    def get_includes(self):
        """Populate a list of HTM includes in the header"""
        for htm in self.root.findall('htmapi'):
            if htm.get('type') == 'header':
                self.htms_include.append(htm.get('target'))
        return self.htms_include

    def get_fixes(self):
        '''Method to populate a list of htm fixes'''
        suggestion_dict = {}
        for sysc in self.root.findall('htmapi'):
            if sysc.get("replacer"):
                suggestion_dict[sysc.get("target")] = (sysc.get("replacer"))
        return suggestion_dict
