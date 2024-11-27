# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bbmap(Package, SourceforgePackage):
    """Short read aligner for DNA and RNA-seq data."""

    homepage = "https://sourceforge.net/projects/bbmap/"
    sourceforge_mirror_path = "bbmap/BBMap_38.63.tar.gz"

    license("BSD-3-Clause-LBNL")

    version("39.01", sha256="98608da50130c47f3abd095b889cc87f60beeb8b96169b664bc9d849abe093e6")
    version("38.63", sha256="089064104526c8d696164aefa067f935b888bc71ef95527c72a98c17ee90a01f")
    version("37.78", sha256="f2da19f64d2bfb7db4c0392212668b425c96a27c77bd9d88d8f0aea90a193509")
    version("37.36", sha256="befe76d7d6f3d0f0cd79b8a01004a2283bdc0b5ab21b0743e9dbde7c7d79e8a9")

    depends_on("c", type="build")  # generated

    depends_on("java")

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)

    def setup_run_environment(self, env):
        env.set("BBMAP_CONFIG", self.prefix.bin.config)
        env.set("BBMAP_RESOURCES", self.prefix.bin.resources)
