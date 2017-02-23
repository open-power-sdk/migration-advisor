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
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""

import ma.checkers.checker_file_utils as utils
from ma.checkers.checker import Checker

class ApiMpiChecker(Checker):
    """ Intel MPI (Message Passing Interface) library API Checker"""

    def __init__(self):
        self.problem_type = "Message Passing Interface API"
        self.problem_msg = "Check usage of Message Passing Interface Library"
        self.mpi_includes = ["mpi.h"]
        self.hint = r"mpi.*\|MPI.*\|Mpi.*"

    def get_pattern_hint(self):
        return self.hint

    def get_problem_msg(self):
        return self.problem_msg

    def get_problem_type(self):
        return self.problem_type

    def check_include(self, include_name):
        if include_name in self.mpi_includes:
            return True

    def check_file(self, file_name):
        statements = utils.get_all_statements(['MPI_.*', 'MPI:.*'], file_name)
        reports = utils.format_statements(statements, ['MPI_.*', 'MPI:.*'])
        return reports
