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
LOCAL_XML_ASM = DIR_PATH + "/../resources/asmtoppc.xml"


class AssemblyReplacer(object):
    """Class to assembly replacer for MA.
    This class get information stored in XML file
    into a python module"""
    def __init__(self):
        self.replacer = {}
        self.load_xml(LOCAL_XML_ASM)


    def load_xml(self, file_name):
        '''Method to load ASM replace strings.
        This method open XML file and load info inside a
        dictionary data structure'''
        tree = elemTree.parse(file_name)
        root = tree.getroot()
        for asm in root.iter('asm'):
            self.replacer[asm.attrib['target']] = [asm.attrib['type'], asm.attrib['replacer']]


    def get_replace(self, target):
        '''Method to get the replace for selected target'''
        return self.replacer[target][1]


    def get_type(self, target):
        '''Method to get the type for selected target'''
        return self.replacer[target][0]
