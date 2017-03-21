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
        * Rafael Peria de Sene <rpsene@br.ibm.com>
"""


import xml.etree.ElementTree as elemTree
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
SYSCALLS_FILE = DIR_PATH + "/../resources/syscalls.xml"


class SyscallsLoader(object):
    ''' Load syscalls into a Python element '''

    def __init__(self):
        self.syscalls = []
        self.__load_xml(SYSCALLS_FILE)

    def __load_xml(self, file_name):
        '''Function to load the contents of syscalls.xml'''
        tree = elemTree.parse(file_name)
        self.root = tree.getroot()
        for sysc in self.root.iter('syscall'):
            self.syscalls.append(sysc.attrib)

    def get_names(self):
        '''Method to populate a list of syscall names '''
        for sysc in self.root.findall('syscall'):
            self.syscalls.append(sysc.get("target"))
        return self.syscalls

    def get_fixes(self):
        '''Method to populate a list of syscall fixes'''
        suggestion_dict = {}
        for sysc in self.root.findall('syscall'):
            if sysc.get("replacer"):
                suggestion_dict[sysc.get("target")] = (sysc.get("replacer"),
                    sysc.get("includes"))
        return suggestion_dict
