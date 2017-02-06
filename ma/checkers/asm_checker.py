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
        * Rafael Peria de Sene <rpsene@br.ibm.com>
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""

from clang.cindex import CursorKind

from ma.checkers.checker import Checker


class AsmChecker(Checker):
    """ Checker for inline assembly declarations """

    def __init__(self):
        super(AsmChecker, self).__init__()
        self.problem_type = "Inline assembly"
        self.problem_msg = "Possible arch specific assembly"
        self.hint = "asm"


    def get_pattern_hint(self):
        return self.hint


    def get_problem_msg(self):
        return self.problem_msg


    def get_problem_type(self):
        return self.problem_type


    def check(self, node):
        return node.kind == (CursorKind.ASM_STMT or CursorKind.MS_ASM_STMT)
