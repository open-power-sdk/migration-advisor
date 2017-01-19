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

import core


class ProblemReporter(object):
    """ Class to handle with reported problems """
    problems = {}

    def report_problem(self, node, problem_type, problem_msg):
        """ Add the reported problem in a dictionary """
        # Do not report if location is not known
        if not node.location.file:
            return

        problem = Problem(node, problem_msg)
        if self.problems.get(problem_type, None) is not None:
            self.problems.get(problem_type).append(problem)
        else:
            problem_list = []
            problem_list.append(problem)
            self.problems[problem_type] = problem_list

    def print_problems(self):
        """ Print all reported problems """
        self.__print_logo()
        for problem_type, problems in self.problems.items():
            print "Problem type: " + problem_type
            print "Problem description: " + problems[0].get_problem_msg()
            for problem in problems:
                print "   Name: " + problem.get_name()
                print "   File: " + str(problem.get_file())
                print "   Line: " + str(problem.get_line())
                print ""

    @classmethod
    def __print_logo(cls):
        """ Print the report logo """
        title = "Migration Report"
        border = "=" * len(title)
        print ""
        print border
        print title
        print border


class Problem(object):
    """ Class to represent a problem """
    def __init__(self, node, problem_msg):
        self.node = node
        self.problem_msg = problem_msg
        self.location = node.location

    def get_node(self):
        """ Get the node (cursor) """
        return self.node

    def get_name(self):
        """ Get the node raw name """
        name = self.node.displayname
        if not name:
            name = self.node.spelling
        # If displayname and spelling do not provide the name of the node,
        # parse the file using the offset information
        if not name:
            ext = self.node.extent
            start = ext.start.offset
            end = ext.end.offset
            length = end - start
            name = core.get_file_content(str(self.get_file()), start, length)
        return name

    def get_problem_msg(self):
        """ Get problem message """
        return self.problem_msg

    def get_file(self):
        """ Get the line path """
        return self.location.file

    def get_line(self):
        """ Get the line """
        return self.location.line
