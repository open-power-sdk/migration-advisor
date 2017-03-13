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

import sys
from clang.cindex import Index
from clang.cindex import TranslationUnit

from checkers.asm_checker import AsmChecker
from checkers.long_double_checker import LongDoubleChecker
from checkers.syscall_checker import SyscallChecker
from checkers.char_checker import CharChecker
from checkers.htm_checker import HtmChecker
from checkers.performance_degradation_checker import PerformanceDegradationChecker
from checkers.api_dfp_checker import ApiDfpChecker
from checkers.api_ipp_checker import ApiIppChecker
from checkers.api_mkl_checker import ApiMklChecker
from checkers.api_mpi_checker import ApiMpiChecker
from checkers.pthread_checker import PthreadChecker
from checkers.builtin_checker import BuiltinChecker
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
    for chk in _load_checkers():
        _run_checker(chk, args.execution_mode, args.location[0])
    ProblemReporter.print_problems()


def _run_checker(checker, mode, set_of_files):
    if mode == 'full':
        files = core.get_files(set_of_files)
    else:
        files = core.get_files(set_of_files, checker.get_pattern_hint())
    if not files:
        cnf = 'Could not find any problem related to '
        cnf += checker.get_problem_type().lower()
        sys.stderr.write(cnf + '\n')
    else:
        print __current_wip(checker, files)
        visitor = Visitor(checker)
        index = Index.create()
        for c_file in files:
            root = index.parse(c_file, options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
            ReportBlocker.blocked_lines = []
            visitor.visit(root.cursor, c_file)


def _load_checkers():
    """ This function load select checker.
    It returns a list with all active checkers """
    api_dfp_checker = ApiDfpChecker()
    api_ipp_checker = ApiIppChecker()
    api_mpi_checker = ApiMpiChecker()
    api_mkl_checker = ApiMklChecker()
    asm_checker = AsmChecker()
    builtin_checker = BuiltinChecker()
    char_checker = CharChecker()
    htm_checker = HtmChecker()
    long_double_checker = LongDoubleChecker()
    perf_degrad_checker = PerformanceDegradationChecker()
    pthread_checker = PthreadChecker()
    syscall_checker = SyscallChecker()

    # Return a list with all active checkers
    return [api_dfp_checker, api_ipp_checker, api_mpi_checker, api_mkl_checker,
            asm_checker, builtin_checker, char_checker, htm_checker,
            long_double_checker, pthread_checker, perf_degrad_checker,
            syscall_checker]


def __current_wip(checker, files):
    wip_msg = 'Looking for ' + checker.get_problem_type().lower()
    wip_msg += ' problems in ' + str(len(files)) + ' suspect files.'
    return wip_msg
