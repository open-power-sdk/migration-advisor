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
import time
from clang.cindex import Index
from clang.cindex import TranslationUnit

from checkers.asm_checker import AsmChecker
from visitor import Visitor
from problem_reporter import ProblemReporter
import core


def run(args):
    """
    Executes the correct action according the user input.

    Parameters:
        args - arguments collected by argparser
    """
    files = __get_files(args.location[0])

    # TODO: checkers need to be inputed by user in argparser
    asm_checker = AsmChecker()

    # List with all active checkers
    checkers = [asm_checker]

    visitor = Visitor(checkers)
    index = Index.create()
    print "Amount of files to be checked: " + str(len(files)) + "\n"
    for c_file in files:
        print "Checking file: " + c_file
        tu = index.parse(c_file, options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
        visitor.visit_nodes(tu.cursor)
    problem_reporter = ProblemReporter()
    problem_reporter.print_problems()


def __get_files(location):
    """ Get a list of supported file names given a location (that can be either
    a file or a directory). If no supported file is found, force to exit """
    files = []
    if os.path.isdir(location):
        files = core.get_files(location)
    elif os.path.isfile(location):
        files.append(location)
    else:
        sys.stderr.write("invalid file or directory: {0}\n".format(location))
        sys.exit(1)

    files = core.get_supported_files(files)
    if not files:
        sys.stderr.write("None of the files provided are supported by "
                         "Migration Advisor. \n")
        sys.exit(1)
    return files
