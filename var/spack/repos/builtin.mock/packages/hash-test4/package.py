# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HashTest4(Package):
    """This package isn't compared with others, but it contains constructs
    that package hashing logic has tripped over in the past.
    """

    homepage = "http://www.hashtest4.org"
    url = "http://www.hashtest1.org/downloads/hashtest4-1.1.tar.bz2"

    version("1.1", md5="a" * 32)

    def install(self, spec, prefix):
        pass

    @staticmethod
    def examine_prefix(pkg):
        pass

    run_after("install")(examine_prefix)
