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


from ma.checkers.checker import Checker

from clang.cindex import CursorKind
from clang.cindex import TypeKind


class LongChecker(Checker):
    """ Checker for long declarations """

    def __init__(self):
        self.problem_type = "Long usage"
        self.problem_msg = "Potential migration issue due size of long"\
                           " variables in Power 64 architecture."
        self.hint = "long"

    def get_pattern_hint(self):
        return self.hint

    def get_problem_msg(self):
        return self.problem_msg

    def get_problem_type(self):
        return self.problem_type

    def check_node(self, node):
        if node.kind != CursorKind.VAR_DECL:
            return False

        node_type_kind = node.type.kind

        if node_type_kind == TypeKind.TYPEDEF:
            node_type_kind = node.type.get_canonical().kind

        return node_type_kind == TypeKind.LONG
