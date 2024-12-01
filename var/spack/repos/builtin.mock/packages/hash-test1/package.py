# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class HashTest1(Package):
    """Used to test package hashing"""

    homepage = "http://www.hashtest1.org"
    url = "http://www.hashtest1.org/downloads/hashtest1-1.1.tar.bz2"

    version("1.1", md5="a" * 32)
    version("1.2", md5="b" * 32)
    version("1.3", md5="c" * 32)
    version("1.4", md5="d" * 32)
    version("1.5", md5="d" * 32)
    version("1.6", md5="e" * 32)
    version("1.7", md5="f" * 32)

    patch("patch1.patch", when="@1.1")
    patch("patch2.patch", when="@1.4")

    variant("variantx", default=False, description="Test variant X")
    variant("varianty", default=False, description="Test variant Y")

    def setup_dependent_build_environment(self, env, dependent_spec):
        pass

    @when("@:1.4")
    def install(self, spec, prefix):
        print("install 1")
        os.listdir(os.getcwd())

        # sanity_check_prefix requires something in the install directory
        mkdirp(prefix.bin)

    @when("@1.5:")
    def install(self, spec, prefix):
        os.listdir(os.getcwd())

        # sanity_check_prefix requires something in the install directory
        mkdirp(prefix.bin)

    @when("@1.5,1.6")
    def extra_phase(self, spec, prefix):
        pass
