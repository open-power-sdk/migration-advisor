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
        * Rafael Sene <rpsene@br.ibm.com>
        * Daniel Kreling <dbkreling@br.ibm.com>
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
        * Roberto Oliveira <rdutra@br.ibm.com>
"""
import subprocess
import time
import re
import os
import sys
import fnmatch


# List of supported x86 patterns
X86_PATTERNS = ["amd64", "AMD64", "[xX]86", "[xX]86_64", "[iI]386", "[iI]486",
                "[iI]686"]

# List of supported ppc patterns
PPC_PATTERNS = ["PPC", "ppc", "power[pP][cC]", "POWER[pP][cC]"]


def get_supported_checkers():
    """Return the supported checkers"""
    return ['api', 'asm', 'builtins', 'char', 'htm', 'performance',
            'pthread', 'syscall', 'double']


def get_supported_extensions():
    """Returns the list of supported extesions on MA"""
    return ['*.cpp', '*.c', '*.h']


def execute(command):
    """ Execute a command with its parameters and return the exit code """
    try:
        return subprocess.check_call([command], stderr=subprocess.STDOUT,
                                     shell=True)
    except subprocess.CalledProcessError as excp:
        return excp.returncode


def execute_stdout(command):
    """ Execute a command with its parameter and return the exit code
    and the command output """
    try:
        output = subprocess.check_output([command], stderr=subprocess.STDOUT,
                                         shell=True)
        return 0, output
    except subprocess.CalledProcessError as excp:
        return excp.returncode, excp.output


def cmdexists(command):
    """Check if a command exists"""
    subp = subprocess.call("type " + command, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return subp == 0


def get_timestamp():
    """Return the current timestamp"""
    return time.strftime("%Y%m%d_%H%M%S")


def get_files(location, hint=''):
    """ Get a list of supported file names given a location (that can be either
    a file or a directory). If no supported file is found, force to exit.
    It also returns all files from a directory that contains the 'hint' when it
    is specified """
    files = []
    if os.path.isdir(location):
        extensions = ' --include=' + \
            ' --include='.join([str(e) for e in get_supported_extensions()])
        cmd = 'grep -rl ' + extensions + ' \''
        cmd += str(hint) + '\' ' + location
        status, files = execute_stdout(cmd)
        return files.split()
    elif os.path.isfile(location):
        for ext in get_supported_extensions():
            if fnmatch.fnmatch(location, ext):
                files.append(location)
        return files
    else:
        sys.stderr.write("Invalid file or directory: {0}\n".format(location))
        sys.exit(1)


def get_file_content(file_name, offset, length):
    """ Read the content of a file given the offset and the length. The offset
    is where the read begins and length is how many characters will be read. If
    length is zero, it returns the entire line content """
    with open(file_name, "rb") as infile:
        infile.seek(offset, 0)
        if length == 0:
            return infile.readline().strip()
        return infile.read(length)


def get_raw_node(node):
    """ Get the raw signature of a node """
    node_file = node.location.file
    ext = node.extent
    start = ext.start.offset
    end = ext.end.offset
    return get_file_content(str(node_file), start, end - start)


def get_includes(file_path):
    """ Get the includes from a C/C++ file and return it as a dictionary with
    include line and name """
    includes_dict = {}
    command = "grep -n '#\s*include' " + file_path
    status, output = execute_stdout(command)
    includes_list = output.strip().split('\n')
    delimiter = ":"
    for include in includes_list:
        if delimiter in include:
            line = int(include.split(delimiter)[0])
            name = include.split(delimiter)[1]
            name = name.replace("#", "").replace("include", "").replace(
                "<", "").replace(">", "").replace("\"", "")
            includes_dict[line] = name.strip()
    return includes_dict


def get_ifdefs(file_path):
    """ Get #ifdef blocks from C/C++ file and and return them in a list of
    lists, where the first element is the line number where the block starts
    and the second element is the block of code """
    with open(file_path) as c_file:
        lines = c_file.readlines()

    ifdef_regex = "#.*if.*defined.*|#.*ifdef.*"
    ifdef_list = []
    num_line = 1
    code_block = ''
    line_block = 0
    inside_block = False
    for line in lines:
        if re.search(ifdef_regex, line) and not inside_block:
            code_block += line
            line_block = num_line
            inside_block = True
        elif re.search("#.*endif", line):
            code_block += line
            ifdef_list.append([line_block, code_block])
            code_block = ''
            inside_block = False
        elif inside_block:
            code_block += line
        num_line += 1

    return ifdef_list


def get_ifdef_regex(arch, separator):
    """ Get the regex to find ifdef blocks for a specific architecture """
    patterns = []
    if arch is "x86":
        patterns = X86_PATTERNS
    elif arch is "ppc":
        patterns = PPC_PATTERNS

    regex = ""
    for pattern in patterns:
        regex += "#.*if.*" + pattern + separator
    regex = regex[:-len(separator)]
    return regex
