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
        * Roberto Oliveira <rdutra@br.ibm.com>
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""

import os
import sys
import time

import core


class Controller(object):
    """
    Controls the execution of MA commands
    """

    def run(self, args):
        """
        Executes the correct action according the user input.

        Parameters:
            args - arguments collected by argparser
        """
        location = args.location[0]

        files = []
        if os.path.isdir(location):
            files = core.get_files(location)
        elif os.path.isfile(location):
            files.append(location)
        else:
            sys.stderr.write("invalid file or directory: {0}\n".format(
                location))
            sys.exit(1)

        files = core.get_supported_files(files)
        if not files:
            sys.stderr.write("None of the files provided are supported by "
                             "Migration Advisor. \n")
            sys.exit(1)

        print "supported files = ", files
        # TODO: at this point "files" variable has all supported files, we need
        # to pass each of them to clang to create the Translation Units
