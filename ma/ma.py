#! /usr/bin/env python
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

import sys
import argparse
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import pkg_resources

from controller import Controller

__all__ = []
__version__ = pkg_resources.require("cpi")[0].version


class CLIError(Exception):
    """Error treatment"""
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):
    """MA main function"""
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_version = "v%s" % __version__
    program_version_message = '%%(prog)s %s ' % (program_version)
    program_shortdesc = '''
    --- Migration Advisor (MA) ---
    Migrates C/C++ applications to POWER
    '''

    try:
        parser = ArgumentParser(description=program_shortdesc,
                                formatter_class=RawTextHelpFormatter)
        parser.add_argument('-V', '--version',
                            action='version',
                            version=program_version_message)
        subparsers = parser.add_subparsers(help='\nMA commands\n\n')

        # Process arguments
        args = parser.parse_args()
        ctrller = Controller()
        ctrller.run(args)
    except KeyboardInterrupt:
        return 1

if __name__ == "__main__":
    sys.exit(main())
