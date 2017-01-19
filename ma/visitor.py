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

import abc


class Visitor(object):
    """ Class used to visit the translation unit nodes and run checkers """

    def __init__(self, checkers_list):
        self.checkers_list = checkers_list

    def visit_nodes(self, node):
        """ Visit all nodes from translation unit and for each node, call all
        activate checkers to seek for problems """
        for checker in self.checkers_list:
            checker.visit(node)
        for n in node.get_children():
            self.visit_nodes(n)

    @abc.abstractmethod
    def visit(self, node):
        """ Visit a node from translation unit """
        raise NotImplementedError("Implement this method in checkers classes")
