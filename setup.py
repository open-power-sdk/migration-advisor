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

from setuptools import setup, find_packages
from pip.req import parse_requirements
import glob
import ma.core

with open('README.md') as f:
    readme = f.read()

requirement_file = './requirements.txt'

if ma.core.cmdexists('clang'):
    clang_installed = glob.glob('/usr/lib*/clang/[0-9].[0-9].[0-9]')
    reverse_list = list(reversed(clang_installed))
    if reverse_list:
        clang_version = reverse_list[0].split('/')[-1][:-2]
        clang_line = 'clang==' + clang_version
        with open(requirement_file, 'a+') as req_file:
            if not any(clang_line in line for line in req_file):
                req_file.write(clang_line + '\n')
else:
    print 'Looks like you do not have clang installed. Install it first.'
    exit(2)

requirements_list = parse_requirements(requirement_file, session=False)
requirements = [str(required.req) for required in requirements_list]

setup(
    name='ma',
    version='1.0.timestamp'+clang_version.replace('.', ''),
    description='Migrates C/C++ applications to POWER',
    long_description=readme,
    author='Rafael Peria de Sene, Roberto Guimarães Dutra de Oliveira, \
Daniel Battaiola Kreling, Diego Fernandez Merjildo',
    author_email='rpsene@br.ibm.com, rdutra@br.ibm.com, \
dbkreling@br.ibm.com, merjildo@br.ibm.com',
    url='https://www-304.ibm.com/webapp/set2/sas/f/lopdiags/sdklop.html',
    license='Apache Software License 2.0',
    install_requires=requirements,
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=['bin/ma'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License 2.0',
          ],
)
