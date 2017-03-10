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

import re
import core


class ReportBlocker(object):
    """ Class deals with blocks that should not be reported, like preprocessors
    blocks with a specific architecture defined """

    # List with lines that should be ignored from report
    blocked_lines = []

    # All preprocessor blocks that should be skipped
    _skip_blocks_regex = ""

    # Preprocessors that represents the end of a block part
    _block_end_regex = "#.*elif.*|#.*else|#.*endif"

    @classmethod
    def block_lines(cls, file_name):
        """ Check all ifdef preprocessors from a file and add lines that
        are inside preprocessors blocks that should not be reported """
        cls._set_skip_blocks()

        ifdef_list = core.get_ifdefs(file_name)
        for ifdef in ifdef_list:
            line = ifdef[0]
            ifdef_block = ifdef[1]

            code_block = ifdef_block.splitlines()
            for i, code in enumerate(code_block):
                line += 1
                if re.search(cls._skip_blocks_regex, code) is not None:
                    lines = cls._get_lines_in_block(code_block[i+1:], line)
                    cls.blocked_lines.extend(lines)

    @classmethod
    def _set_skip_blocks(cls):
        """ Set preprocessor blocks that should be skipped """
        if cls._skip_blocks_regex:
            return
        sep = "|"
        cls._skip_blocks_regex = core.get_ifdef_regex("x86", sep)
        cls._skip_blocks_regex += sep + core.get_ifdef_regex("ppc", sep)

    @classmethod
    def _get_lines_in_block(cls, code_block, line):
        """ Get lines that are inside the current preprocessor block. The code
        block is a list with the code and the line is the first line inside the
        preprocessor """
        lines = []
        for code in code_block:
            if re.search(cls._block_end_regex, code):
                break
            lines.append(line)
            line += 1
        return lines
