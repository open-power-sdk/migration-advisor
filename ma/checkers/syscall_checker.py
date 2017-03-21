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
        * Roberto Oliveira <rdutra@br.ibm.com>
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
        * Rafael Peria de Sene <rpsene@br.ibm.com>
"""

from ma.checkers.checker import Checker
from ma.xml_loader.syscalls_loader import SyscallsLoader
from clang.cindex import CursorKind


class SyscallChecker(Checker):
    """ Checker for syscall declarations """

    def __init__(self):
        self.problem_type = "Syscall usage"
        self.problem_msg = "Syscall not available in Power architecture."
        self.hint = 'ch[s/g/l/f/v/o/m/]\|SYS_\|' + 'statat'
        self.syscalls_names = SyscallsLoader().get_names()
        self.syscalls_fixes = SyscallsLoader().get_fixes()

    def get_pattern_hint(self):
        return self.hint

    def get_problem_msg(self):
        return self.problem_msg

    def get_problem_type(self):
        return self.problem_type

    def check_node(self, node):
        if node.kind == CursorKind.CALL_EXPR:
            if node.displayname in self.syscalls_names:
                return True

    def get_solution(self, node):
        if node.displayname in self.syscalls_fixes:
            return self.__create_solution(node)

    def __create_solution(cls, node):
        fix = cls.syscalls_fixes[node.displayname]
        fix_msg = "Replace " + node.displayname + " for " + fix[0]
        if fix[1]:
            fix_msg += " and include " + fix[1]
        return fix_msg
