# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class HashTest2(Package):
    """Used to test package hashing"""

    homepage = "http://www.hashtest2.org"
    url = "http://www.hashtest1.org/downloads/hashtest2-1.1.tar.bz2"

    version("1.1", sha256="a" * 64)
    version("1.2", sha256="b" * 64)

    # Source hash differs from hash-test1@1.3
    version("1.3", sha256=("c" * 63) + "f")

    version("1.4", sha256="d" * 64)

    patch("patch1.patch", when="@1.1")

    variant("variantx", default=False, description="Test variant X")
    variant("varianty", default=False, description="Test variant Y")

    def setup_dependent_build_environment(self, env, dependent_spec):
        pass

    def install(self, spec, prefix):
        print("install 1")
        os.listdir(os.getcwd())

        # sanity_check_prefix requires something in the install directory
        mkdirp(prefix.bin)
