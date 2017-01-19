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

from ma.problem_reporter import ProblemReporter
from ma.visitor import Visitor
from clang.cindex import CursorKind


class AsmChecker(Visitor):
    """ Checker for inline assembly declarations """

    def __init__(self):
        self.reporter = ProblemReporter()
        self.problem_type = "Inline assembly"
        self.problem_msg = "Possible arch specific assembly"

    def visit(self, node):
        if node.kind == (CursorKind.ASM_STMT or CursorKind.MS_ASM_STMT):
            self.reporter.report_problem(node, self.problem_type,
                                         self.problem_msg)
