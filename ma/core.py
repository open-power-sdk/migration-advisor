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
import commands
import time
import sys


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
        subprocess.check_output([command], stderr=subprocess.STDOUT,
                                shell=True)
        return 0, ""
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
