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
from ma import core


class PerformanceDegradationChecker(Checker):
    """ This checker finds preprocessor ifs with architecture
    optimizations and without an optimization for Linux on Power"""

    def __init__(self):
        super(PerformanceDegradationChecker, self).__init__()
        self.problem_type = "Performance degradation"
        self.problem_msg = "This preprocessor can contain code without Power optimization"
        self.hint = self.__get_x86_hint("\\|")
        self.ppc = self.__get_ppc_hint()
        self.x86 = self.__get_x86_hint("|")

    def get_pattern_hint(self):
        return self.hint

    def get_problem_msg(self):
        return self.problem_msg

    def get_problem_type(self):
        return self.problem_type

    def check_file(self, filename):
        ifdef_lst = core.get_ifdefs(filename)
        if not ifdef_lst:
            return []

        report_list = []
        for code_block in ifdef_lst:
            num_line = code_block[0]
            code = code_block[1]

            # PPC part is already in the block
            if re.search(self.ppc, code) is not None:
                continue

            for line in code.splitlines():
                # x86 part in the block
                if re.search(self.x86, line) is not None:
                    report_list.append([line, num_line])
                num_line += 1
        return report_list

    @classmethod
    def __get_x86_hint(cls, sep):
        """ Return hint for x86 ifdef blocks """
        hint = "\\#.*if.*amd64" + sep + "\\#.*if.*AMD64" + sep
        hint += "\\#.*if.*[xX]86" + sep + "\\#.*if.*[xX]86_64" + sep
        hint += "\\#.*if.*[iI]386" + sep + "\\#.*if.*[iI]486" + sep
        hint += "\\#.*if.*[iI]686" + sep
        hint += "\\#.*if.*intel" + sep + "\\#.*if.*INTEL"
        return hint

    @classmethod
    def __get_ppc_hint(cls):
        """ Return hint for ppc ifdef blocks """
        hint = "\\#.*if.*PPC|\\#.*if.*ppc|\\#.*if.*powerPC|"
        hint += "\\#.*if.*power[pP][cC]|\\#.*if.*POWER[pP][cC]"
        return hint
