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
DFP_API_FILE = DIR_PATH + "/../resources/api_dfp_quickfix.xml"


class ApiDfpLoader(object):
    """ Load api_dfp_quickfix.xml information into a Python element"""

    def __init__(self):
        self.item_names = []
        self.item_targets = []
        self.item_types = []
        self.__load_xml(DFP_API_FILE)

    def __load_xml(self, file_name):
        """ Load the contents of api_dfp_quickfix.xml into a Python element"""
        tree = elemTree.parse(file_name)
        self.root = tree.getroot()
        self.__load_names()
        self.__load_types()
        self.__load_targets(self.root)

    def __load_names(self):
        for tag in self.root:
            self.item_names.append(tag.attrib['name'])

    def __load_types(self):
        for item in self.root.iter("item"):
            self.item_types.append(item.attrib['type'])

    def __load_targets(self, root):
        for item in root.iter("item"):
            self.item_targets.append(item.attrib['target'])
