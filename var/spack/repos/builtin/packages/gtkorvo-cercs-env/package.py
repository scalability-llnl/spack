# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GtkorvoCercsEnv(CMakePackage):
    """A utility library used by some GTkorvo packages."""

    homepage = "https://github.com/GTkorvo/cercs_env"
    url      = "https://github.com/GTkorvo/cercs_env/archive/v1.0.tar.gz"
    git      = "https://github.com/GTkorvo/cercs_env.git"

    version('develop', branch='master')
    version('1.0', '08f0532d0c2f7bc9b53dfa7a1c40ea4d')

    def cmake_args(self):
        args = ["-DENABLE_TESTING=0", "-DENABLE_SHARED_STATIC=STATIC"]
        return args
