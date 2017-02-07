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

import core
from report_blocker import ReportBlocker


class ProblemReporter(object):
    """ Class to handle with reported problems """
    problems = {}

    @classmethod
    def report_problem(cls, node, current_file, problem_type, problem_msg):
        """ Add the reported problem in a dictionary """
        if not cls.__should_report(node, current_file):
            return

        problem = Problem(node, problem_msg)
        if cls.problems.get(problem_type, None) is not None:
            cls.problems.get(problem_type).append(problem)
        else:
            problem_list = []
            problem_list.append(problem)
            cls.problems[problem_type] = problem_list

    @classmethod
    def print_problems(cls):
        """ Print all reported problems """
        cls.__print_logo()
        for problem_type, problems in cls.problems.items():
            print "Problem type: " + problem_type
            print "Problem description: " + problems[0].get_problem_msg()
            for problem in problems:
                print "   Name: " + problem.get_name()
                print "   File: " + str(problem.get_file())
                print "   Line: " + str(problem.get_line())
                print ""

    def get_problems(self):
        """ Get all reported problems """
        return self.problems

    def clear_problems(self):
        """ Clear reported problems """
        self.problems.clear()

    @classmethod
    def __should_report(cls, node, current_file):
        """ Check if should report the node """
        node_loc = node.location
        node_file = node_loc.file
        # Location is not known
        if not node_file:
            return False
        # Node is not in the current file
        if str(node_file) != current_file:
            return False
        # Node is inside a blocked line
        if node_loc.line in ReportBlocker.blocked_lines:
            return False
        return True

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
