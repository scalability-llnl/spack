# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Typescript(Package):
    """TypeScript is a superset of JavaScript that compiles to clean JavaScript output."""

    homepage = "https://www.typescriptlang.org"
    url = "https://github.com/microsoft/TypeScript/archive/refs/tags/v5.3.2.tar.gz"

    license("Apache-2.0")

    version("5.3.2", sha256="c5a12507006e7d2b8020dec9589191ce070fd88203f2c80aca00d641cee7866f")

    depends_on("node-js", type=("build", "link", "run"))
    depends_on("npm", type="build")

    def install(self, spec, prefix):
        npm = which("npm", required=True)
        npm("install", "--global", f"--prefix={prefix}")
