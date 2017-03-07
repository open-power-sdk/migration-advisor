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
from ma import core

LINE_DELIMITER = "$"


def _get_lines(names, file_name):
    """ Get all lines that contain names and return it as a list """
    grep_delimiter = "\\|"
    command = "grep -n '"
    for name in names:
        command += name + grep_delimiter
    command = command[:-len(grep_delimiter)]
    command += "' " + file_name + " | cut -f1 -d:"
    lines = core.execute_stdout(command)[1]
    return lines.split()


def get_all_statements(names, file_name):
    """ Get all statements from a file that contains specific names. The
    parameter 'names' is a list of names that will be searched in the file.
    This function returns a list with the line number and the statement, e.g:
        <line_number>$<statement>
     """
    # Split list to avoid problem with command size
    size = 2500
    names = [names[x: x + size] for x in xrange(0, len(names), size)]

    lines = []
    for name in names:
        lines.extend(_get_lines(name, file_name))

    # If lines list is empty it avoid to use Awk and return an empty list
    if not lines:
        return []

    # Run awk command to get entire statements from problematic lines
    awk_delimiter = '||'
    command = "awk '"
    for line in lines:
        command += "NR==" + line + awk_delimiter
    command = command[:-len(awk_delimiter)]
    command += ",/;/ {print NR\"" + LINE_DELIMITER + "\", $0}' " + file_name
    output = core.execute_stdout(command)[1]

    # Parse the output and join lines that are part of the same statement
    statements = []
    statement = ''
    # take out Windows End of line.
    output = output.replace("\r\n", "\n")
    # take out Mac systems Carriage return.
    output = output.replace("\r", "\n")

    first_line = True
    for out in output.strip().split("\n"):
        if ";" in out:
            if "\n" in statement:
                statement += out.split(LINE_DELIMITER)[1]
            else:
                statement += out
            statements.append(statement)
            statement = ''
            first_line = True
        else:
            if first_line:
                statement += out + "\n"
                first_line = False
            else:
                statement += out.split(LINE_DELIMITER)[1] + "\n"
    return statements


def format_statements(statements, names):
    """ Format statements by the minimum size make it valid and return a list
    of lists, in which each list contains the line number and the minimum valid
    statement

    The parameter 'statements' is a list of statements to be formatted and
    should be in format: <line_number>$<statement>
    The parameter 'names' is a list of names used to format the statement and
    get the minimum valid statement.

    Formatting e.g:
        parameter 'names' contains "int"
        code:       int x = 10;
        formatting: int x

        parameter 'names' contains "sum"
        code:       int x = sum(y, z);
        formatting: sum(y, z)
    """
    formatted_statements = []
    for report in statements:
        if LINE_DELIMITER not in report:
            return formatted_statements
        line = int(report.split(LINE_DELIMITER)[0])
        content = report.split(LINE_DELIMITER)[1].strip()

        # Split statement and keep the delimiters
        is_macro = False
        tokens = re.split('(\\(| |=|;|\\t|\\n|#|{)', content)
        for index, token in enumerate(tokens):
            # If is a line break, increment line count
            if token == "\n":
                line += 1
            # The line is a macro
            if token == "define":
                is_macro = True

            if _check_token(token, names) is False:
                continue

            statement_end = [";", "=", "{"]
            # If is a macro, the statement can ends in a break line
            if is_macro:
                statement_end.append("\n")
                is_macro = False

            # Assemble the statement
            while not any(x in token for x in statement_end):
                index += 1
                token += tokens[index]
            # Remove the delimiter and extra spaces
            statement = token[:-1]
            statement = statement.strip()
            formatted_statements.append([statement, line])
    return formatted_statements


def _check_token(token, names):
    """ Checks if a token exists in names list.
    As some versions of regex module only support groups of 100, this method splits the
    names in sub-groups in order to check the token. Best case scenario, the token will
    be found in the first 100 elements. In the worst case, it will go through all the l
    ist as usual. """

    max_regex = 99
    grouped_names = [names[i: i + max_regex] for i in xrange(0, len(names), max_regex)]
    for sub_names in grouped_names:
        regexes = "(" + ")|(".join(sub_names) + ")"
        if re.match(regexes, token) is not None:
            return True
    return False
