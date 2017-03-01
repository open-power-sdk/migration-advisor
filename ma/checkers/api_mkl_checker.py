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
from ma.xml_loader.api_mkl_loader import ApiMklLoader


class ApiMklChecker(Checker):
    """ Intel MKL (Math Kernel Library) library API Checker"""

    def __init__(self):
        self.problem_type = "Math Kernel Library API"
        self.problem_msg = "Check usage of Intel Math Kernel Library API"
        self.mkl_includes = ["mkl.h", "mkl.*.h"]
        self.hint = r"mkl.*\|MKL.*\|Mkl.*"
        self.mkl_values = ApiMklLoader().mkl_values

    def get_pattern_hint(self):
        return self.hint

    def get_problem_msg(self):
        return self.problem_msg

    def get_problem_type(self):
        return self.problem_type

    def check_include(self, include_name):
        if include_name in self.mkl_includes:
            return True

    def check_file(self, file_name):
        values = self.mkl_values['function'] + self.mkl_values['type']
        statements_type = utils.get_all_statements(self.mkl_values['type'], file_name)
        statements_function = utils.get_all_statements(self.mkl_values['function'], file_name)
        statements = statements_type + statements_function
        return  utils.format_statements(statements, values)
