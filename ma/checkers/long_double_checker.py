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

from ma.problem_reporter import ProblemReporter
from ma.checkers.checker import Checker
from clang.cindex import CursorKind
from clang.cindex import TypeKind


class LongDoubleChecker(Checker):
    """ Checker for long double declarations """

    def __init__(self):
        self.reporter = ProblemReporter()
        self.problem_type = "Long double usage"
        self.problem_msg = "Potential migration issue due size of long double"\
                           " variables in Power architecture."

    def check(self, node):
        if node.kind != CursorKind.VAR_DECL:
            return 0

        node_type = node.type
        node_kind = node_type.kind
        if node_kind == TypeKind.TYPEDEF:
            node_kind = node.type.get_canonical().kind

        if node_kind == TypeKind.LONGDOUBLE:
            self.reporter.report_problem(node, self.problem_type,
                                         self.problem_msg)
