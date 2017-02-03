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
"""

from ma.checkers.checker import Checker
from ma.xml_loader.syscalls_loader import SyscallsLoader
from clang.cindex import CursorKind
from clang.cindex import TypeKind


class SyscallChecker(Checker):
    """ Checker for syscall declarations """

    def __init__(self):
        super(SyscallChecker, self).__init__()
        self.problem_type = "Syscall usage"
        self.problem_msg = "Syscall not available in Power architecture."
        self.hint = 'ch[s/g/l/f/v/o/m/]\|[A-Za-z][0-9]\|' + 'statat'
        self.syscalls_names = SyscallsLoader().get_names()

    def get_pattern_hint(self):
        """ Returns a regex to match all 32 and all 64 bits syscalls"""
        return self.hint

    def get_problem_msg(self):
        return self.problem_msg

    def get_problem_type(self):
        return self.problem_type

    def check(self, node):
        """ Return true if a call expression is one of the problematic syscalls"""
        if node.kind != CursorKind.CALL_EXPR:
            return False

        if node.displayname in self.syscalls_names:
            return True
