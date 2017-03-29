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
"""

import ma.checkers.checker_file_utils as utils
from ma.checkers.checker import Checker
from ma.xml_loader.builtins_loader import BuiltinLoader


class BuiltinChecker(Checker):
    """ Checker for x86-specific built-ins """

    def __init__(self):
        self.problem_type = "x86-specific compiler built-in"
        self.problem_msg = "x86 built-ins not supported in Power"
        self.loader = BuiltinLoader()
        self.builtins_names = self.loader.builtins_names
        self.builtins_headers = self.loader.builtins_headers

    def get_pattern_hint(self):
        delimiter = "\|"
        headers_hint = delimiter.join(self.builtins_headers)

        # Change names that have same pattern for a regex
        regex = ("__builtin", "_mm", "_m_")
        names = [x for x in self.builtins_names if not x.startswith(regex)]
        names.extend(regex)
        names_hint = delimiter.join(names)
        return names_hint + delimiter + headers_hint

    def get_problem_msg(self):
        return self.problem_msg

    def get_problem_type(self):
        return self.problem_type

    def check_file(self, file_name):
        statements = utils.get_all_statements(self.builtins_names, file_name)
        return utils.format_statements(statements, self.builtins_names)

    def check_include(self, include_name):
        return self.loader.is_builtin(include_name)
