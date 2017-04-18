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
        * Rafael Peria de Sene <rpsene@br.ibm.com>
"""

import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DOC_FILE = DIR_PATH + "/resources/information/"


class HelpCreator(object):
    '''Creates help messages explainging each checker'''

    def create_help(self, checker):
        '''Creates the help message show when users select
           ma info -c <checker>
        '''
        print '\n' + self.format_help(checker) + '\n'

    @classmethod
    def format_help(cls, checker):
        '''Formats the help message show when users select
           ma info -c <checker>
        '''
        fpath = DOC_FILE + checker
        try:
            with open(fpath, 'r') as help_msg:
                return help_msg.read()
        except IOError:
            print "Could not read file:", fpath
