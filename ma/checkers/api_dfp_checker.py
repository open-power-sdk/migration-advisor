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
        * Daniel Kreling <dbkreling@br.ibm.com>
"""
import ma.checkers.checker_file_utils as utils

from ma.checkers.checker import Checker
from ma.xml_loader.api_dfp_loader import ApiDfpLoader


class ApiDfpChecker(Checker):
    """ Checker for Decimal Floating Point (DFP) API """

    def __init__(self):
        self.problem_type = "Decimal Floating Point (DFP) API"
        self.problem_msg = "x86 API not supported in Power"
        self.api_dfp_names = ApiDfpLoader().item_names
        self.api_dfp_targets = ApiDfpLoader().item_targets
        self.api_dfp_includes = ["bid_functions.h"]

    def get_pattern_hint(self):
        delimiter = "\|"
        dfp_hint = delimiter.join(self.api_dfp_targets)
        return dfp_hint

    def get_problem_msg(self):
        return self.problem_msg

    def get_problem_type(self):
        return self.problem_type

    def check_include(self, include_name):
        if include_name in self.api_dfp_includes:
            return True

    def check_file(self, file_name):
        statements = utils.get_all_statements(self.api_dfp_targets, file_name)
        return utils.format_statements(statements, self.api_dfp_targets)
