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
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import pkg_resources

import controller

__all__ = []
__version__ = pkg_resources.require("ma")[0].version


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

        parser_run = subparsers.add_parser(
            'run',
            formatter_class=RawTextHelpFormatter,
            help='Analyze project for possible migration problems.\n'
                 'see ma run --help\n\n')

        parser_info = subparsers.add_parser(
            'info',
            formatter_class=RawTextHelpFormatter,
            help='See information about possible checkers.\n'
                 'see ma info --help\n\n')

        parser_run.add_argument(
            dest='location',
            metavar='LOCATION',
            help='file or directory where the files to be migrated are',
            nargs=1)
        parser_run.add_argument(
            '-m', '--mode',
            dest='execution_mode',
            type=str,
            choices=['full', 'lightweight'], default='lightweight',
            help='specify the execution mode of MA which can be \'full\' or\n'
            '\'lightweight\'. The \'full\' mode looks for problems in all files\n'
            'located in a given directory. This option may take several minutes\n'
            'to complete. In the other hand the \'lightweight\' mode minimize\n'
            'the amount of files where the search for problems is executed by\n'
            'best guessing whether a file should or not be verified.\n'
            '    e.g: ma run --mode=full <location>')
        parser_run.add_argument(
            '-s', '--stat',
            dest='statistics',
            type=str,
            choices=['project', 'file'], default='',
            help='display migration statistics by project or per file'
                 '\nThis option suppresses the migraton report')

        # Process arguments
        args = parser.parse_args()
        controller.run(args)
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    sys.exit(main())
