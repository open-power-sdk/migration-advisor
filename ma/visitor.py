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

import os
from clang.cindex import CursorKind

from report_blocker import ReportBlocker
from problem_reporter import ProblemReporter
import core


class Visitor(object):
    """ Class used to visit the translation unit nodes and run checkers """

    def __init__(self, checker):
        self.checker = checker
        self.current_file = ''
        self.files_treat_list = ["Performance degradation",
                                 "Decimal Floating Point (DFP) API",
                                 "Integrated Performance Primitives (IPP) API",
                                 "Math Kernel Library (MKL) API",
                                 "Message Passing Interface (MPI) API",
                                 "Non Portable Pthread",
                                 "x86-specific compiler built-in"]

    def visit(self, node, file_name):
        """ Run checker accordingly, either using the TranslationUnit Unit or
        a file """
        self.current_file = file_name
        ReportBlocker.block_lines(self.current_file)

        self.visit_includes()
        if self.checker.get_problem_type() in self.files_treat_list:
            self.visit_file()
        else:
            self.visit_nodes(node)

    def visit_nodes(self, node):
        """ Visit all nodes from translation unit and for each node, call all
        activate checkers to seek for problems """
        if self.checker.check_node(node):
            ProblemReporter.report_node(node, self.current_file,
                                        self.checker.get_problem_type(),
                                        self.checker.get_problem_msg(),
                                        self.checker.get_solution(node))

        for node in node.get_children():
            self.visit_nodes(node)

    def visit_includes(self):
        """ Visit includes from translation unit and for each include, call
        all activate checkers to seek for problems """
        includes_dict = core.get_includes(self.current_file)
        for line, name in includes_dict.items():
            name = os.path.basename(name)
            if self.checker.check_include(name):
                ProblemReporter.report_include(name, self.current_file, line,
                                               self.checker.get_problem_type(),
                                               self.checker.get_problem_msg(),
                                               self.checker.get_solution(name))

    def visit_file(self):
        """ Visit files and look for problems that clang doesn't treat """
        reports = self.checker.check_file(self.current_file)
        for report in reports:
            name = report[0]
            num_line = report[1]
            ProblemReporter.report_file(self.current_file, num_line, name,
                                        self.checker.get_problem_type(),
                                        self.checker.get_problem_msg(),
                                        self.checker.get_solution(name))
