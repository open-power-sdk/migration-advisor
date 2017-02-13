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
        self.files_treat_list = ["Performance degradation"]

    def visit(self, node):
        """ Visit all nodes from translation unit and for each node, call all
        activate checkers to seek for problems """

        if self.checker.get_problem_type() in self.files_treat_list:
            self.visit_file()
        else:
            self.visit_nodes(node)

        self.visit_includes(core.get_includes(self.current_file))

    def visit_nodes(self, node):
        """ Visit all nodes from translation unit and for each node, call all
        activate checkers to seek for problems """
        if node.kind == CursorKind.MACRO_INSTANTIATION:
            ReportBlocker.check_node(node, self.current_file)

        if self.checker.check_node(node):
            ProblemReporter.report_node(node, self.current_file,
                                        self.checker.get_problem_type(),
                                        self.checker.get_problem_msg())

        for node in node.get_children():
            self.visit_nodes(node)

    def visit_includes(self, includes_dict):
        """ Visit includes from translation unit and for each include, call
        all activate checkers to seek for problems """
        for line, name in includes_dict.items():
            name = os.path.basename(name)
            if self.checker.check_include(name):
                ProblemReporter.report_include(name, self.current_file, line,
                                               self.checker.get_problem_type(),
                                               self.checker.get_problem_msg())

    def visit_file(self):
        """ Visit a file and look for problems that clang doesn't treat"""
        problem_type = self.checker.get_problem_type()
        problem_msg = self.checker.get_problem_msg()

        ifdef_list = self.checker.check_file(self.current_file)
        for code_block in ifdef_list:
            num_and_problm = (''.join(code_block.keys())).strip(' \t\n\r')
            num_line = num_and_problm.split(":")[0]
            name = num_and_problm.split(":")[1]
            ProblemReporter.report_file(self.current_file,
                                        num_line,
                                        name,
                                        problem_type,
                                        problem_msg)

    def set_current_file(self, file_name):
        """ Set the name of the current file that is being visited """
        self.current_file = file_name
