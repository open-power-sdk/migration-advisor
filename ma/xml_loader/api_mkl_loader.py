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
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""

import xml.etree.ElementTree as elemTree
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
LOCAL_XML_MKL = DIR_PATH + "/../resources/mkl_api.xml"


class ApiMklLoader(object):
    """Class to load Math Kernel Library targets for MA.
    This class get information stored in XML file
    into a python module"""
    def __init__(self):
        self._mkl_values = {}
        self.load_xml(LOCAL_XML_MKL)

    def load_xml(self, file_name):
        '''Method to load target strings.
        This method open XML file and load info inside a
        dictionary data structure'''
        tree = elemTree.parse(file_name)
        root = tree.getroot()
        self._mkl_values['type'] = []
        self._mkl_values['function'] = []

        for item in root.iter(tag='item'):
            self._mkl_values[item.attrib['type']].append(item.attrib['target'])

    @property
    def mkl_values(self):
        """ Retung Mkl values from XML"""
        return self._mkl_values
