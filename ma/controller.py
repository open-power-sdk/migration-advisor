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
        * Rafael Sene <rpsene@br.ibm.com>
        * Daniel Kreling <dbkreling@br.ibm.com>
        * Roberto Oliveira <rdutra@br.ibm.com>
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""

import os
import sys
import fnmatch
from clang.cindex import Index
from clang.cindex import TranslationUnit

from checkers.asm_checker import AsmChecker
from checkers.long_double_checker import LongDoubleChecker
from checkers.syscall_checker import SyscallChecker
from visitor import Visitor
from problem_reporter import ProblemReporter
from report_blocker import ReportBlocker
import core


def run(args):
    """
    Executes the correct action according the user input.

    Parameters:
        args - arguments collected by argparser
    """

    files_locations = args.location[0]

    checkers = _load_checkers()

    for chk in checkers:
        _run_checker(chk, files_locations)

    ProblemReporter.print_problems()


def _run_checker(checker, set_of_files):
    files = __get_files(set_of_files, checker.get_pattern_hint())
    print __current_wip(checker, files)
    visitor = Visitor(checker)
    index = Index.create()
    for c_file in files:
        root = index.parse(c_file, options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
        ReportBlocker.blocked_lines = []
        visitor.visit_nodes(root.cursor)


def _load_checkers():
    """ This function load select checker.
    It returns a list with all active checkers """

    asm_checker = AsmChecker()
    long_double_checker = LongDoubleChecker()
    syscall_checker = SyscallChecker()

    # List with all active checkers
    return [asm_checker, long_double_checker, syscall_checker]


def __current_wip(checker, files):
    wip_msg = 'Looking for ' + checker.get_problem_type().lower()
    wip_msg += ' problems in ' + str(len(files)) + ' suspect files.'
    return wip_msg


def __get_files(location, hint):
    """ Get a list of supported file names given a location (that can be either
    a file or a directory). If no supported file is found, force to exit """
    files = []
    if os.path.isdir(location):
        files = core.get_files(location, hint)
    elif os.path.isfile(location):
        for ext in core.get_supported_extensions():
            if fnmatch.fnmatch(location, ext):
                files.append(location)
    else:
        sys.stderr.write("Invalid file or directory: {0}\n".format(location))
        sys.exit(1)
    if not files:
        sys.stderr.write("None of the files provided are supported by "
                         "Migration Advisor. \n")
        sys.exit(1)
    return files
