# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Antlr(AutotoolsPackage):
    """ANTLR (ANother Tool for Language Recognition) is a powerful parser
    generator for reading, processing, executing, or translating structured
    text or binary files. It's widely used to build languages, tools, and
    frameworks. From a grammar, ANTLR generates a parser that can build and
    walk parse trees."""

    homepage = "https://www.antlr2.org/"
    url = "https://www.antlr2.org/download/antlr-2.7.7.tar.gz"

    license("ANTLR-PD")

    version("2.7.7", sha256="853aeb021aef7586bda29e74a6b03006bcb565a755c86b66032d8ec31b67dbb9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Fixes build with recent versions of GCC
    patch("gcc.patch")

    variant("cxx", default=True, description="Enable ANTLR for C++")
    variant("java", default=False, description="Enable ANTLR for Java")
    variant("python", default=False, description="Enable ANTLR for Python")
    variant("pic", default=False, description="Enable fPIC")

    extends("python", when="+python")
    depends_on("java", type=("build", "run"), when="+java")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+pic"):
            env.set("CXXFLAGS", "-fPIC")

    def configure_args(self):
        args = ["--disable-csharp"]
        args.extend(self.enable_or_disable("cxx"))
        args.extend(self.enable_or_disable("java"))
        args.extend(self.enable_or_disable("python"))

        return args
