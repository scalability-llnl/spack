# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ploticus(MakefilePackage):
    """Ploticus can produce various types of plots and graphs."""

    homepage = "https://ploticus.sourceforge.net/doc/welcome.html"

    maintainers("Christoph-TU")

    version("2.42", sha256="3f29e4b9f405203a93efec900e5816d9e1b4381821881e241c08cab7dd66e0b0")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")
    depends_on("libpng")

    build_directory = "src"

    def url_for_version(self, version):
        # spack's default url_for_version may replace "242_src" with 2.42_src, causing a 404.
        # Returning the correct url here instead of as 'url =' fixes this issue:
        return (
            "https://sourceforge.net/projects/ploticus/files/ploticus/2.42/ploticus242_src.tar.gz"
        )

    def setup_run_environment(self, env):
        env.set("PLOTICUS_PREFABS", self.prefix.prefabs)

    def edit(self, spec, prefix):
        makefile = FileFilter("src/Makefile")
        makefile.filter("CC = .*", "CC = {0}".format(spack_cc))

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.prefabs)
        install("src/pl", prefix.bin)
        install_tree("prefabs", prefix.prefabs)
