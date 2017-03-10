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
        self.hint = core.get_ifdef_regex("x86", "\\|")
        self.ppc = core.get_ifdef_regex("ppc", "|")
        self.x86 = core.get_ifdef_regex("x86", "|")

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
