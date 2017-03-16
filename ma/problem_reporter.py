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
    def report_include(cls, name, file_name, line, problem_type, problem_msg):
        """ Report a problem in an include directive """
        if not cls.__should_report(file_name, line, file_name):
            return
        name = "include " + name
        problem = Problem(name, file_name, line, problem_msg)
        cls.__report_problem(problem, problem_type)

    @classmethod
    def report_node(cls, node, current_file, problem_type, problem_msg):
        """ Report a problem in a node """
        node_loc = node.location
        node_file = node_loc.file
        node_line = node_loc.line
        if not cls.__should_report(node_file, node_line, current_file):
            return

        ext = node.extent
        start = ext.start.offset
        end = ext.end.offset
        name = core.get_file_content(str(node_file), start, end - start)

        problem = Problem(name, node_file, node_line, problem_msg)
        cls.__report_problem(problem, problem_type)

    @classmethod
    def report_file(cls, file_name, num_line, name,
                    problem_type, problem_msg):
        """ Report a problem in a file """
        if not cls.__should_report(file_name, num_line, file_name):
            return
        problem = Problem(name, file_name, num_line, problem_msg)
        cls.__report_problem(problem, problem_type)

    @classmethod
    def __report_problem(cls, problem, problem_type):
        """ Add the reported problem in a dictionary """
        if cls.problems.get(problem_type, None) is not None:
            cls.problems.get(problem_type).append(problem)
        else:
            problem_list = []
            problem_list.append(problem)
            cls.problems[problem_type] = problem_list

    @classmethod
    def print_problems(cls):
        """ Print all reported problems """
        if not cls.problems:
            print "\nNo migration reports found."
            return

        TAB = "   "
        cls.__print_logo()
        for problem_type, problems in cls.problems.items():
            problems_dict = {}
            # Group problems by file
            for problem in problems:
                name = problem.file_name
                problems_dict[name] = problems_dict.get(name, []) + [problem]

            print "Problem type: " + problem_type
            print "Problem description: " + problems[0].problem_msg
            for file_name, problems in problems_dict.items():
                print TAB + "File: " + file_name
                for problem in problems:
                    print (TAB * 2) + "Problem: " + problem.name
                    print (TAB * 2) + "Line: " + str(problem.line)
                    print ""
            print ""

    @classmethod
    def get_problems(cls):
        """ Get all reported problems """
        return cls.problems

    @classmethod
    def clear_problems(cls):
        """ Clear reported problems """
        cls.problems.clear()

    @classmethod
    def __should_report(cls, node_file, node_line, current_file):
        """ Check if should report the node """
        # Location is not known
        if not node_file:
            return False
        # Node is not in the current file
        if str(node_file) != current_file:
            return False
        # Node is inside a blocked line
        if node_line in ReportBlocker.blocked_lines:
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
    def __init__(self, name, file_name, line, problem_msg):
        self._name = name
        self._file_name = str(file_name)
        self._line = line
        self._problem_msg = problem_msg

    @property
    def name(self):
        """ Raw name """
        return self._name

    @property
    def problem_msg(self):
        """ Problem message """
        return self._problem_msg

    @property
    def file_name(self):
        """ File name """
        return self._file_name

    @property
    def line(self):
        """ Line number """
        return self._line
