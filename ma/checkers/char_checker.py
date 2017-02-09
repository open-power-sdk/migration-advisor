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

from clang.cindex import CursorKind
from clang.cindex import TypeKind

from ma.checkers.checker import Checker


class CharChecker(Checker):
    """ Checker for char usage problems """

    def __init__(self):
        self.problem_type = "Char usage"
        self.problem_msg = "This statement may cause different result in "\
            "Power architecture because char variables are unsigned by default"
        self.hint = "char"

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

        if self.is_dangerous_type(node) and self.has_children(node):
            last_children_node = list(node.get_children())[-1]
            return self.is_dangerous_assignment(last_children_node)

    def has_children(self, node):
        """ Check if node has children """
        return len(list(node.get_children()))

    def is_dangerous_type(self, node):
        """ Check if node type can be a dangerous type. For this checker it
        can be dangerous if it is only char (without signed or unsigned) """
        node_type = node.type
        node_type_kind = node_type.kind
        if node_type_kind == TypeKind.TYPEDEF:
            node_type_kind = node_type.get_canonical().kind

        if node_type_kind in (TypeKind.CHAR_U, TypeKind.CHAR_S):
            return True

    def is_dangerous_assignment(self, node, is_dangerous=True):
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
            return self.is_dangerous_assignment(children, is_dangerous)
        else:
            return is_dangerous
