# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BuildEnvCompilerVarB(Package):
    """Package with runtime variable that should be dropped in the parent's build environment."""

    url = "https://www.example.com"
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def setup_run_environment(self, env):
        env.set("CC", "this-should-be-dropped")
        env.set("CXX", "this-should-be-dropped")
        env.set("FC", "this-should-be-dropped")
        env.set("F77", "this-should-be-dropped")
        env.set("ANOTHER_VAR", "this-should-be-present")
