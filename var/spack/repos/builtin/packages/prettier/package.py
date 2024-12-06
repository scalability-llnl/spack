# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Prettier(Package):
    """Prettier is an opinionated code formatter."""

    homepage = "https://prettier.io/"
    url = "https://github.com/prettier/prettier/archive/refs/tags/3.2.5.tar.gz"

    maintainers("adamjstewart")
    license("MIT")

    version("3.2.5", sha256="0ac58fbe50859feb06099670526460cef7f51c83fee458b02fc67e53ffd23f57")

    depends_on("node-js", type=("build", "run"))
    depends_on("npm", type="build")

    def install(self, spec, prefix):
        npm = which("npm", required=True)
        npm("install", "--global", f"--prefix={prefix}")
