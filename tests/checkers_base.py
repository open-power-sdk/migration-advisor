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
"""


from clang.cindex import Index
from clang.cindex import TranslationUnit

from ma.visitor import Visitor
from ma.problem_reporter import ProblemReporter
from ma import core


class CheckersBase():
    """ Base class to use checkers test """
    def __init__(self):
        self.reporter = ProblemReporter()

    def run(self, checker, path):
        """ Run the test setup which includes the creation of the syntax tree
        and the run of checker. The checker is the one that will be activated
        and the path is the folder with the files used in the test """
        self.reporter.clear_problems()
        visitor = Visitor(checker)
        index = Index.create()
        files = core.get_files(path, checker.get_pattern_hint())
        for f in files:
            tu = index.parse(f, options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
            visitor.set_current_file(f)
            visitor.visit_includes(core.get_includes(f))
            visitor.visit_nodes(tu.cursor)

    def get_reported_lines(self):
        """ Return a list of lines that were reported """
        problems = self.reporter.get_problems()
        lines = []
        for problem in problems.values()[0]:
            lines.append(problem.line)
        return lines
