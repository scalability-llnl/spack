# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SameVersionAs(Package):
    """Simple package that is used to test same_version_as-directive.

    See same_version_as_wrapper package as well.
    """

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', 'hash1')
    version('2.0', 'hash2')
    version('3.0', 'hash3')
    version('4.0', 'hash4')

    parallel = False
