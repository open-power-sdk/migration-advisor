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
        * Daniel Kreling <dbkreling@br.ibm.com>
        * Rafael Peria de Sene <rpsene@br.ibm.com>
"""

import os
import unittest

from ma.checkers.asm_checker import AsmChecker
from ma.checkers.long_double_checker import LongDoubleChecker
from ma.checkers.syscall_checker import SyscallChecker
from ma.checkers.long_checker import LongChecker
from ma.checkers.char_checker import CharChecker
from ma.checkers.htm_checker import HtmChecker
from ma.checkers.performance_degradation_checker import PerformanceDegradationChecker
from ma.checkers.api_dfp_checker import ApiDfpChecker
from ma.checkers.api_ipp_checker import ApiIppChecker
from ma.checkers.api_mkl_checker import ApiMklChecker
from ma.checkers.api_mpi_checker import ApiMpiChecker
from ma.checkers.pthread_checker import PthreadChecker
from ma.checkers.builtin_checker import BuiltinChecker
from checkers_base import CheckersBase


class Checkers(unittest.TestCase):
    """ Test class to run checkers """

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.resources_folder = dir_path + "/resources/"
        self.base = CheckersBase()

    def inline_asm_test(self):
        """ Inline assembly tests """
        folder = self.resources_folder + "asm"
        self.base.run(AsmChecker(), folder)
        expected_lines = [5, 6, 7]
        self.__check_lines(expected_lines)

    def long_double_test(self):
        """ Long double declaration tests """
        folder = self.resources_folder + "long_double"
        self.base.run(LongDoubleChecker(), folder)
        expected_lines = [2, 5, 8]
        self.__check_lines(expected_lines)

    def syscalls_test(self):
        """ Syscalls not supported in Power tests """
        folder = self.resources_folder + "syscalls"
        self.base.run(SyscallChecker(), folder)
        expected_lines = range(2, 38)
        self.__check_lines(expected_lines)

    def long_test(self):
        """ Long declarations test"""
        folder = self.resources_folder + "long"
        self.base.run(LongChecker(), folder)
        expected_lines = [2, 5, 8]
        self.__check_lines(expected_lines)

    def char_test(self):
        """ Char usage tests """
        folder = self.resources_folder + "char"
        self.base.run(CharChecker(), folder)
        expected_lines = []
        expected_lines.extend(range(48, 60))
        expected_lines.extend(range(65, 79))

    def htm_test(self):
        """ HTM calls not supported in Power tests """
        folder = self.resources_folder + "htm"
        self.base.run(HtmChecker(), folder)
        expected_lines = [1, 5, 7, 9]
        self.__check_lines(expected_lines)

    def perf_degrad_test(self):
        """ Performance degradation usage tests """
        folder = self.resources_folder + "perf_degrad"
        self.base.run(PerformanceDegradationChecker(), folder)
        expected_lines = [6, 14, 38, 46, 52, 64, 74, 92, 98]
        self.__check_lines(expected_lines)

    def api_dfp_test(self):
        """ Test for DFP API calls not supported in Power """
        folder = self.resources_folder + "api/dfp"
        self.base.run(ApiDfpChecker(), folder)
        expected_lines = [1, 5, 6, 8, 8, 10, 10, 12, 13, 14, 15, 16]
        self.__check_lines(expected_lines)

    def api_ipp_test(self):
        """ Test for IPP API calls not supported in Power """
        folder = self.resources_folder + "api/ipp"
        self.base.run(ApiIppChecker(), folder)
        expected_lines = [1] + range(4, 15)
        self.__check_lines(expected_lines)

    def api_mkl_test(self):
        """ Math Kernel Library API checker tests """
        folder = self.resources_folder + "api/mkl"
        self.base.run(ApiMklChecker(), folder)
        expected_lines = [1, 8, 18, 22, 23, 24, 26, 27, 28, 8, 36,
                          37, 38, 42, 43, 44, 45]
        self.__check_lines(expected_lines)

    def api_mpi_test(self):
        """ Message Passing Interface usage tests """
        folder = self.resources_folder + "api/mpi"
        self.base.run(ApiMpiChecker(), folder)
        expected_lines = [1, 4, 6, 8, 10, 12, 13, 18, 19]

    def pthread_test(self):
        """ Test for no portable Pthreads """
        folder = self.resources_folder + "pthread"
        self.base.run(PthreadChecker(), folder)
        expected_lines = [5, 6, 7, 12, 13, 18, 19]
        self.__check_lines(expected_lines)

    def builtin_test(self):
        """ x86 Built-in tests """
        folder = self.resources_folder + "builtin"
        self.base.run(BuiltinChecker(), folder)
        expected_lines = [2, 3, 9, 10, 12, 13, 14, 14, 15, 16, 17]
        self.__check_lines(expected_lines)

    def __check_lines(self, expected_lines):
        """ Auxiliar method to check if reported lines match to the expected
        lines. If it does not match, test fails """
        reported_lines = self.base.get_reported_lines()
        self.assertItemsEqual(expected_lines, reported_lines)


if __name__ == '__main__':
    unittest.main()
