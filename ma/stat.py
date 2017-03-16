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
        # TODO: Implement me!

    def _print_logo(self, title):
        """ Print the statistics logo """
        border = "=" * len(title)
        print ""
        print border
        print title
        print border
