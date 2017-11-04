[![Build Status](https://travis-ci.org/open-power-sdk/migration-advisor.svg?branch=master)](https://travis-ci.org/open-power-sdk/migration-advisor)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/83083b5dcfe647bb8ccc05a48decafb6)](https://www.codacy.com/app/rpsene/migration-advisor?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=open-power-sdk/migration-advisor&amp;utm_campaign=Badge_Grade)

# Project Description

The Migration Advisor helps on moving Linux applications to Power Systems servers.
Its locates potential migration problems within a C/C++ project, such as source code
that might produce different results when run on Power Systems servers.

The current version of Migration Advisor are able to detect the following migration problems:

Linux/x86-specific API

x86-specific assembly

x86-specific compiler built-in

Char usage

Long double usage

Hardware Transaction Memory

Performance degradation

Non-portable Pthreads implementation

Syscall not available for Linux on Power

For more information about MA usage, see ma --help

## Contributing to the project
We welcome contributions to the Migration Advisor Project in many forms. There's always plenty to do! Full details of how to contribute to this project are documented in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Maintainers
The project's [maintainers](MAINTAINERS.txt): are responsible for reviewing and merging all pull requests and they guide the over-all technical direction of the project.

## Communication <a name="communication"></a>
We use [Slack](https://toolsforpower.slack.com/) for communication.

## Supported Architecture and Operating Systems
x86_64 and ppc64le: Ubuntu 16.04, CentOS7, RHEL 7.3, Fedora 25.

## Installing
Requirements: python-pip, python-pylint, python-virtualenv, python-docsutil, clang

Testing: ./dev tests

Build: ./dev release

Build and install: ./dev install

Execution: ma --help

## Documentation

usage: ma [-h] [-V] {run,info} ...

run          analyze a given directory or file for possible C/C++
             migration problems from x86_64 to Power
             see ma run --help

info         show information about supported migration checkers
             see ma info --help

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit


## Still Have Questions?
For general purpose questions, please use [StackOverflow](http://stackoverflow.com/questions/tagged/toolsforpower).

## License <a name="license"></a>
The Migration Advisor Project uses the [Apache License Version 2.0](LICENSE) software license.
