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

import re
from ma.checkers.checker import Checker

class PerformanceDegradationChecker(Checker):
    """ This checker finds preprocessor ifs with architecture
    optimizations and without an optimization for Linux on Power"""

    def __init__(self):
        super(PerformanceDegradationChecker, self).__init__()
        self.problem_type = "Performance degradation"
        self.problem_msg = "This preprocessor can contain code without Power optimization"
        self.hint = self.__set_hint("\\|")
        self.ppc = "\\#.*if.*PPC|\\#.*if.*ppc|\\#.*if.*powerPC|"
        self.ppc += "\\#.*if.*power[pP][cC]|\\#.*if.*POWER[pP][cC]"

    def get_pattern_hint(self):
        return self.hint

    def get_problem_msg(self):
        return self.problem_msg

    def get_problem_type(self):
        return self.problem_type

    def check_node(self, node):
        pass

    def check_file(self, filename):
        with open(filename) as c_file:
            lines = c_file.readlines()
        ifdef_lst = self.__get_ifdefs(lines)
        ret_lst = []

        if not ifdef_lst:
            return []

        for code_block in ifdef_lst:
            # Look for Power declaration
            if re.search(self.ppc, code_block.values()[0]) is None:
                ret_lst.append(code_block)
        return ret_lst

    @classmethod
    def __get_ifdefs(cls, lines):
        """ This method receives a C source code as lines.
        Find blocks #ifdef and save it in a list of dict"""
        hint = cls.__set_hint("|")
        ifdef_list = []
        code_block = ''
        headline = ''

        num_line = 1
        for line in lines:
            if re.search(hint, line):
                code_block = ''
                headline = str(num_line) + ":" + line
            elif line.find("#endif") != -1 and re.search(hint, headline):
                block = {}
                block[headline] = code_block
                ifdef_list.append(block)
                headline = ''
            elif headline:
                code_block += line

            num_line += 1

        return ifdef_list

    @classmethod
    def __set_hint(cls, sep):
        """ Return hint regular expresion for Grep use or Python"""
        hint = "\\#.*if.*amd64" + sep + "\\#.*if.*AMD64" + sep
        hint += "\\#.*if.*[xX]86" + sep + "\\#.*if.*[xX]86_64" + sep
        hint += "\\#.*if.*[iI]386" + sep + "\\#.*if.*[iI]486" + sep
        hint += "\\#.*if.*[iI]686" + sep
        hint += "\\#.*if.*intel" + sep + "\\#.*if.*INTEL"
        return hint
