# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SameVersionAsWrapper(Package):
    """Simple package that is used to test same_version_as-directive.

    See same_version_as_wrapper package as well.
    """

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('4.0', 'hash4')
    version('3.1', 'hash3.1')
    version('3.0', 'hash3.0')
    version('2.2', 'hash2.2')
    version('2.1', 'hash2.1')
    version('2.0', 'hash2')
    version('1.0', 'hash1')

    same_version_as("same_version_as", pkg_to_dep_version=lambda v: v.up_to(1))

    parallel = False
