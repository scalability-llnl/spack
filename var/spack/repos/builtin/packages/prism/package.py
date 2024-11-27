# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Prism(MakefilePackage):
    """PRISM is a probabilistic model checker, a tool for formal modelling and
    analysis of systems that exhibit random or probabilistic behaviour."""

    homepage = "https://www.prismmodelchecker.org/"
    url = "https://github.com/prismmodelchecker/prism/archive/v4.5.tar.gz"

    maintainers("snehring")

    license("GPL-2.0-only")

    version("4.7", sha256="16186047ba49efc6532de6e9c3993c8c73841a7c76c99758d6ee769e72092d6d")
    version("4.5", sha256="1cb7a77538b5c997d98a8c209030c46f9e8f021f7a8332e5eb2fd3b4a23936fd")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    build_directory = "prism"

    depends_on("java@9:", type=("build", "run"))
    depends_on("java@9:11", type=("build", "run"), when="@:4.5")

    patch("Makefile.patch", when="target=aarch64:")

    def setup_run_environment(self, env):
        env.set("PRISM_DIR", self.prefix)

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            # after building, remove PRISM_DIR lines from startup scripts,
            # as they point to the stage and not the prefix
            for f in ["prism", "xprism"]:
                filter_file("^PRISM_DIR.*", "", "bin/{0}".format(f))

            dirs = ["bin", "classes", "dtds", "etc", "include", "images", "lib"]

            for d in dirs:
                install_tree(d, join_path(prefix, d))
