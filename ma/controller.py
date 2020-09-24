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
import subprocess
import glob
from clang.cindex import Index
from clang.cindex import Config
from clang.cindex import TranslationUnit
clang_library_file = ''

from .checkers.asm_checker import AsmChecker
from .checkers.long_double_checker import LongDoubleChecker
from .checkers.syscall_checker import SyscallChecker
from .checkers.char_checker import CharChecker
from .checkers.htm_checker import HtmChecker
from .checkers.performance_degradation_checker import PerformanceDegradationChecker
from .checkers.api_dfp_checker import ApiDfpChecker
from .checkers.api_ipp_checker import ApiIppChecker
from .checkers.api_mkl_checker import ApiMklChecker
from .checkers.api_mpi_checker import ApiMpiChecker
from .checkers.pthread_checker import PthreadChecker
from .checkers.builtin_checker import BuiltinChecker
from .visitor import Visitor
from .stat import Statistics
from .problem_reporter import ProblemReporter
from .report_blocker import ReportBlocker
from .help import HelpCreator
from . import core


def run(argv):
    """
    Executes the correct action according the user input.

    Parameters:
        argv - arguments collected by argparser
    """

    if 'checker_info' in argv:
        chelp = HelpCreator()
        chelp.create_help(argv.checker_info)
        sys.exit(0)
    for chk in _load_checkers(argv.checkers):
        _run_checker(chk, argv)

    statistics = argv.statistics
    if statistics:
        statistic = Statistics(statistics)
        statistic.stat()
    else:
        ProblemReporter.print_problems()

def _include_paths():
    include_paths = []
    try:
        null = open("/dev/null")
        output = subprocess.check_output(["gcc", "-v", "-E", "-"], stdin=null, stderr=subprocess.STDOUT, shell=False)
    except subprocess.CalledProcessError as ex:
        print(ex.cmd)
        print(ex.output)
        return include_paths

    save = False
    for line in output.decode().split('\n'):
        if line == 'End of search list.':
                save=False
        if save:
                include_paths.append("-I" + line.lstrip())
        if line == '#include <...> search starts here:':
                save=True

    return include_paths


def _run_checker(checker, argv):
    global clang_library_file
    if argv.execution_mode == 'full':
        files = core.get_files(argv.location[0])
    else:
        files = core.get_files(argv.location[0], checker.get_pattern_hint())
    if not files:
        cnf = 'Could not find any problem related to '
        cnf += checker.get_problem_type().lower()
        sys.stderr.write(cnf + '\n')
    else:
        print(__current_wip(checker, files))
        visitor = Visitor(checker)
        if clang_library_file == '':
            clang_libraries = glob.glob('/usr/lib64/libclang.so*') + glob.glob('/usr/lib64/llvm/libclang.so') + glob.glob('/usr/lib*/*/libclang-[0-9]*.so.*')
            reverse_list = list(reversed(sorted(clang_libraries)))
            if reverse_list:
                clang_library_file = reverse_list[0]
                Config.set_library_file(clang_library_file)
        index = Index.create()
        for c_file in files:
            args = ["-ferror-limit=9999"] + _include_paths()
            root = index.parse(c_file, args=args, options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
            ReportBlocker.blocked_lines = []
            visitor.visit(root.cursor, c_file)


def _load_checkers(checkers):
    """ This function load select checker.
    It returns a list with all active checkers """
    choosen_checkers = []
    run_checkers = []
    if not isinstance(checkers, list):
        choosen_checkers = checkers.split(',')
    else:
        choosen_checkers = checkers

    if 'api' in choosen_checkers:
        api_dfp_checker = ApiDfpChecker()
        run_checkers.append(api_dfp_checker)
        api_ipp_checker = ApiIppChecker()
        run_checkers.append(api_ipp_checker)
        api_mpi_checker = ApiMpiChecker()
        run_checkers.append(api_mpi_checker)
        api_mkl_checker = ApiMklChecker()
        run_checkers.append(api_mkl_checker)
    if 'asm' in choosen_checkers:
        asm_checker = AsmChecker()
        run_checkers.append(asm_checker)
    if 'builtin' in choosen_checkers:
        builtin_checker = BuiltinChecker()
        run_checkers.append(builtin_checker)
    if 'char' in choosen_checkers:
        char_checker = CharChecker()
        run_checkers.append(char_checker)
    if 'htm' in choosen_checkers:
        htm_checker = HtmChecker()
        run_checkers.append(htm_checker)
    if 'double'in choosen_checkers:
        long_double_checker = LongDoubleChecker()
        run_checkers.append(long_double_checker)
    if 'performance' in choosen_checkers:
        perf_degrad_checker = PerformanceDegradationChecker()
        run_checkers.append(perf_degrad_checker)
    if 'pthread' in choosen_checkers:
        pthread_checker = PthreadChecker()
        run_checkers.append(pthread_checker)
    if 'syscall' in choosen_checkers:
        syscall_checker = SyscallChecker()
        run_checkers.append(syscall_checker)
    # Return a list with all active checkers
    return run_checkers


def __current_wip(checker, files):
    wip_msg = 'Looking for ' + checker.get_problem_type().lower()
    wip_msg += ' problems in ' + str(len(files)) + ' suspect files.'
    return wip_msg
