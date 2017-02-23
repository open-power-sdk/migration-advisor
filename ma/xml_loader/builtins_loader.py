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
        * Roberto Oliveira <rdutra@br.ibm.com>
"""

import os
import xml.etree.ElementTree as elemTree

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
BUILTINS_FILE = DIR_PATH + "/../resources/builtins.xml"


class BuiltinLoader(object):
    """ Class to load builtins from xml file """

    def __init__(self):
        self.builtins = []
        self.__load_builtins(BUILTINS_FILE)
        self._builtins_names = []
        self.__load_builtins_names()
        self._builtins_headers = []
        self.__load_builtins_headers()

    @property
    def builtins_names(self):
        """ Builtins names (functions and data types) """
        return self._builtins_names

    @property
    def builtins_headers(self):
        """ Builtins headers """
        return self._builtins_headers

    def is_builtin(self, name):
        """ Check if the given name is a builtin """
        if name in self.builtins:
            return True

    def __load_builtins_names(self):
        """ Load builtins name (do not include headers) """
        for builtin in self.builtins:
            if isinstance(builtin, Type) or isinstance(builtin, Function):
                self._builtins_names.append(builtin.name)

    def __load_builtins_headers(self):
        """ Load builtins headers """
        for builtin in self.builtins:
            if isinstance(builtin, Include):
                self._builtins_headers.append(builtin.name)

    def __load_builtins(self, file_name):
        """ Load all builtins elements """
        tree = elemTree.parse(file_name)
        root = tree.getroot()
        self.__load_includes(root)
        self.__load_types(root)
        self.__load_functions(root)

    def __load_includes(self, root):
        """ Load includes elements """
        for incl in root.iter('include'):
            name = incl.attrib['name']
            replacer = incl.text
            include = Include(name, replacer)
            self.builtins.append(include)

    def __load_types(self, root):
        """ Load types elements """
        for dtype in root.iter('type'):
            name = dtype.attrib['name']
            replacer = dtype.text
            data_type = Type(name, replacer)
            self.builtins.append(data_type)

    def __load_functions(self, root):
        """ Load functions elements """
        for func in root.iter('function'):
            name = func.attrib['name']
            try:
                finput = func.find(".//in").text
            except AttributeError:
                finput = ""
            try:
                foutput = func.find(".//out").text
            except AttributeError:
                foutput = ""

            code_list = []
            for c in func.iter('code'):
                endian = c.attrib['endian']
                nlines = c.attrib['nlines']
                replacer = c.text
                code = Function.Code(endian, nlines, replacer)
                code_list.append(code)
            function = Function(name, finput, foutput, code_list)
            self.builtins.append(function)


class Builtin(object):
    """ Represents a builtin """
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """ Target name """
        return self._name

    def __eq__(self, name):
        return self.name == name


class Include(Builtin):
    """ Represents a builtin include """
    def __init__(self, name, replacer):
        Builtin.__init__(self, name)
        self._replacer = replacer

    @property
    def replacer(self):
        """ Replacer value """
        return self._replacer


class Type(Builtin):
    """ Represents a builtin type """
    def __init__(self, name, replacer):
        Builtin.__init__(self, name)
        self._replacer = replacer

    @property
    def replacer(self):
        """ Replacer value """
        return self._replacer


class Function(Builtin):
    """ Represents a builtin function """
    def __init__(self, name, finput, foutput, code):
        Builtin.__init__(self, name)
        self._finput = finput
        self._foutput = foutput
        self._code = code

    @property
    def finput(self):
        """ Function input """
        return self._finput

    @property
    def foutput(self):
        """ Function output """
        return self._foutput

    @property
    def code(self):
        """ Replacer code """
        return self._code

    class Code(object):
        """ Represents a code tag from xml that composes a function """
        def __init__(self, endinan, nlines, replacer):
            self._endian = endinan
            self._nlines = nlines
            self._replacer = replacer

        @property
        def endian(self):
            """ Replacer endianness """
            return self._endian

        @property
        def nlines(self):
            """ Replacer number of lines """
            return self._nlines

        @property
        def replacer(self):
            """ Raw replacer """
            return self._replacer
