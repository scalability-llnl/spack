##############################################################################
# Copyright 2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *

class Creduce(CMakePackage):
    """C-Reduce is a tool that takes a large C, C++, or OpenCL file that has a
    property of interest (such as triggering a compiler bug) and automatically
    produces a much smaller C/C++ file that has the same property. It is
    intended for use by people who discover and report bugs in compilers and
    other tools that process source code."""

    homepage = "https://embed.cs.utah.edu/creduce/"
    url      = "https://github.com/csmith-project/creduce"
    git      = "https://github.com/csmith-project/creduce"

    version('develop', branch='master')
    version('2.10.0', tag='creduce-2.10.0')

    depends_on('flex')
    depends_on('libxml2')
    depends_on('llvm@8.0.0', when='@:2.10.999')
    depends_on('perl')
    depends_on('perl-exporter-lite')
    depends_on('perl-file-which')
    depends_on('perl-getopt-tabular')
    depends_on('perl-regexp-common')
    depends_on('perl-term-readkey')
    depends_on('zlib')
