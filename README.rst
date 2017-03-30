Migration Advisor - MA
========================

The Migration Advisor helps on moving Linux applications to Power Systems servers.
Its locates potential migration problems within a project, such as source code that
might produce different results when run on Power Systems servers.

The current version contains the followings checkers:

* Linux/x86-specific API
* x86-specific assembly
* x86-specific compiler built-in
* Char usage
* Long double usage
* Hardware Transaction Memory
* Performance degradation
* Non-portable Pthreads implementation
* Syscall not available for Linux on Power


MA commands:
========================

* run: analyze a given directory or file for possible C/C++ migration problems
       from x86_64 to Power
       see ma run --help

* info: show information about supported migration checkers
        see ma info --help


Supported Architecture and Operating Systems
=========================

* ppc64le: Ubuntu 16.04, CentOS7, RHEL 7.3, Fedora 25.
* x86_64: Ubuntu 16.04, CentOS7, RHEL 7.3, Fedora 25.


Building and Testing
=========================

Requirements: python-pip, python-pylint, python-virtualenv, python-docsutil,
              clang, libclang python bindings.

              IMPORTANT: libclang and clang must have the same version.

Testing: ./dev tests

Build: ./dev release

Build and install: ./dev install


Integrators
=========================

If you intend to integrate MA within your development environemt you should be
aware of the following error codes:

0: no problems occurred

1: generic error code.

2: some dependency tool is missing
