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


class ReportBlocker(object):
    """ Class deals with blocks that should not be reported, like preprocessors
    blocks with a specific architecture defined """

    # All preprocessor blocks that should be skipped
    X86_BLOCKS = ["x86", "x86_64", "i386", "i486", "i686", "amd64"]
    PPC_BLOCKS = ["ppc", "powerpc"]
    SKIP_BLOCKS = X86_BLOCKS + PPC_BLOCKS

    # Preprocessors that represents the end of a block part
    BLOCK_END = ["#elif", "#else", "#endif"]

    # List with lines that should be ignored from report
    blocked_lines = []

    @classmethod
    def check_node(cls, node, current_file):
        """ Check if node is inside a preprocessor block that should not be
        reported. If it is, add to blocked lines """
        name = node.displayname.lower()
        if any(x in name for x in cls.SKIP_BLOCKS):
            node_loc = node.location
            node_file = str(node_loc.file)
            # Just add blocked line if node is inside the current file
            if node_file == current_file:
                line = node_loc.line
                start = node.extent.start.offset
                lines = cls.__get_lines_in_block(node_file, start, line)
                cls.blocked_lines.extend(lines)

    @classmethod
    def __get_lines_in_block(cls, file_name, offset, line):
        """ Get lines that are inside the current preprocessor block.
        The offset is where the preprocessor starts and the line is the line
        where preprocessor is """
        lines = []
        with open(file_name, 'r') as infile:
            infile.seek(offset)
            for content in infile:
                if any(x in content for x in cls.BLOCK_END):
                    break
                lines.append(line)
                line += 1
        return lines
