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
        * Rafael Sene <rpsene@br.ibm.com>
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""

from clang.cindex import CursorKind

from report_blocker import ReportBlocker

from problem_reporter import ProblemReporter

class Visitor(object):
    """ Class used to visit the translation unit nodes and run checkers """

    def __init__(self, checker):
        self.checker = checker

    def visit_nodes(self, node):
        """ Visit all nodes from translation unit and for each node, call all
        activate checkers to seek for problems """
        if node.kind == CursorKind.MACRO_INSTANTIATION:
            ReportBlocker.check_node(node)

        if self.checker.check(node):
            ProblemReporter.report_problem(node,
                                           self.checker.get_problem_type(),
                                           self.checker.get_problem_msg())

        for node in node.get_children():
            self.visit_nodes(node)
