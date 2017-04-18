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
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""
import re
import os
from clang.cindex import CursorKind
from clang.cindex import TypeKind

from ma.checkers.checker import Checker
from ma import core


class CharChecker(Checker):
    """ Checker for char usage problems """

    def __init__(self):
        self.problem_type = "Char usage"
        self.problem_msg = "This statement may cause different result in "\
            "Power architecture because char variables are unsigned by default"
        self.hint = "char"
        self.default_solution = "Change 'char' type to 'signed char'"

    def get_pattern_hint(self):
        return self.hint

    def get_problem_msg(self):
        return self.problem_msg

    def get_problem_type(self):
        return self.problem_type

    def check_node(self, node):
        kind = node.kind
        if kind != CursorKind.BINARY_OPERATOR and kind != CursorKind.VAR_DECL:
            return False

        if self._is_dangerous_type(node) and self._has_children(node):
            last_children_node = list(node.get_children())[-1]
            return self._is_dangerous_assignment(last_children_node)

    def get_solution(self, node):
        kind = node.kind
        type_kind = node.type.kind
        info = ""
        if kind == CursorKind.BINARY_OPERATOR or type_kind == TypeKind.TYPEDEF:
            node = self._get_var_declaration(node, node)
            location = node.location
            line = location.line
            file_name = os.path.basename(str(location.file))
            info = "    (file: {0} | line: {1})".format(file_name, line)

        raw_node = core.get_raw_node(node)
        char_regex = "\\bchar\\b"
        solution = ""
        if (re.search(char_regex, raw_node) and
                not re.search("typedef.*(struct|union)", raw_node)):
            solution = re.sub(char_regex, "signed char", raw_node)
            solution += info
        else:
            solution = self.default_solution
        return solution

    def _get_var_declaration(self, node, definition):
        """ Get where a variable is defined and return the corresponding
        node """
        aux_node = None
        if node.type.kind == TypeKind.TYPEDEF:
            aux_node = node.type.get_declaration()
        elif node.kind == CursorKind.DECL_REF_EXPR:
            aux_node = node.get_definition()

        if aux_node:
            node = aux_node
            definition = node

        for children in node.get_children():
            return self._get_var_declaration(children, definition)

    @staticmethod
    def _has_children(node):
        """ Check if node has children """
        return len(list(node.get_children()))

    @staticmethod
    def _is_dangerous_type(node):
        """ Check if node type can be a dangerous type. For this checker it
        can be dangerous if it is only char (without signed or unsigned) """
        node_type = node.type
        node_type_kind = node_type.kind
        if node_type_kind == TypeKind.TYPEDEF:
            node_type_kind = node_type.get_canonical().kind
        if node_type_kind in (TypeKind.CHAR_U, TypeKind.CHAR_S):
            return True

    def _is_dangerous_assignment(self, node, is_dangerous=True):
        """ Check if the assignment can cause an invalid result in ppc """
        kind = node.kind
        if kind in (CursorKind.CHARACTER_LITERAL, CursorKind.STRING_LITERAL):
            return False

        type_kind = node.type.kind
        if kind == CursorKind.TYPE_REF:
            type_kind = node.type.get_canonical().kind
        if type_kind == TypeKind.POINTER:
            type_kind = node.type.get_pointee().kind
        if type_kind in (TypeKind.CHAR_U, TypeKind.UCHAR, TypeKind.CHAR_S):
            is_dangerous = False
        else:
            is_dangerous = True

        for children in node.get_children():
            return self._is_dangerous_assignment(children, is_dangerous)
