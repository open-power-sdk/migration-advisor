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

from problem_reporter import ProblemReporter
from terminaltables import AsciiTable


class Statistics(object):
    """ Class to deal with statistics """

    def __init__(self, kind):
        self.kind = kind
        self.problems = ProblemReporter.get_problems()

    def stat(self):
        """ Run statistics feature based on the statistic kind """
        if not self.problems:
            print "\nNo statistics to display since no problem was found."
            return

        if self.kind == "project":
            self._stat_project()
        elif self.kind == "file":
            self._stat_file()

    def _stat_project(self):
        """ Run statistics based on overral project """
        title = "Statistics - Project"
        self._print_logo(title)

        table_data = [["Problem", "Amount"]]
        for kind, problems in self.problems.items():
            table_data.append([kind, str(len(problems))])

        stat_table = AsciiTable(table_data)
        stat_table.justify_columns = {0: 'left', 1: 'center'}
        print stat_table.table

    def _stat_file(self):
        """ Run statistics per file """
        title = "Statistics - Per File"
        self._print_logo(title)

        # Get all files that have problems
        files = []
        for problems in self.problems.values():
            for problem in problems:
                file_name = problem.file_name
                if file_name not in files:
                    files.append(problem.file_name)

        # Calculate the amount of problems in each file
        data_dict = {}
        for f in files:
            problem_dict = {}
            for kind, problems in self.problems.items():
                for problem in problems:
                    if problem.file_name == f:
                        problem_dict[kind] = problem_dict.get(kind, 0) + 1
            data_dict[f] = problem_dict

        # Create table data
        table_data = [["File", "Total Amount", "Problems"]]
        for file_name, problems_dict in data_dict.items():
            total_ammount = 0
            problem = ""
            for kind, ammount in problems_dict.items():
                total_ammount += ammount
                problem += str(ammount) + " " + kind + "\n"
            else:
                table_data.append([file_name, total_ammount, problem.strip()])

        stat_table = AsciiTable(table_data)
        stat_table.inner_row_border = True
        stat_table.justify_columns = {0: 'left', 1: 'center', 2: 'left'}
        print stat_table.table

    def _print_logo(self, title):
        """ Print the statistics logo """
        border = "=" * len(title)
        print ""
        print border
        print title
        print border
