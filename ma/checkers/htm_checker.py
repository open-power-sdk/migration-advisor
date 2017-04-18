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

from clang.cindex import CursorKind
from ma.checkers.checker import Checker
from ma.xml_loader.htm_loader import HtmLoader


class HtmChecker(Checker):
    """ Checker for HTM calls. """

    def __init__(self):
        self.problem_type = "Hardware Transactional Memory (HTM)"
        self.problem_msg = "x86 specific HTM calls are not supported in Power Systems"
        self.htm_functions = HtmLoader().get_functions()
        self.htm_includes = HtmLoader().get_includes()
        self.htm_fixes = HtmLoader().get_fixes()
        self.hint = self.__get_hint()

    def get_pattern_hint(self):
        return self.hint

    def get_problem_msg(self):
        return self.problem_msg

    def get_problem_type(self):
        return self.problem_type

    def check_node(self, node):
        if node.kind != CursorKind.CALL_EXPR:
            return False
        if node.displayname in self.htm_functions:
            return True

    def check_include(self, include_name):
        if include_name in self.htm_includes:
            return True

    def get_solution(self, node):
        return self.__create_solution(node)

    def __create_solution(self, node):
        if 'rtmintrin.h' in str(node):
            return "replace rtmintrin.h for htmintrin.h"
        if not isinstance(node, basestring):
            if node.displayname in self.htm_fixes:
                fix = self.htm_fixes[node.displayname]
                return "replace " + node.displayname + " for " + fix

    def __get_hint(self):
        """Create the self.hint string"""
        incl_hint = "\|".join(HtmLoader().get_includes())
        func_hint = "\|".join(self.htm_functions)
        return incl_hint + "\|" + func_hint
