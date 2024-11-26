# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dbxtool(MakefilePackage):
    """tool for managing dbx updates installed on a machine."""

    homepage = "https://github.com/rhboot/dbxtool"
    url = "https://github.com/rhboot/dbxtool/archive/dbxtool-8.tar.gz"

    license("GPL-2.0-only")

    version("8", sha256="196d9475f7cf3aa52d8e0c29c20affb7c903512e13895edb6296caf02d4a983b")
    version("7", sha256="486b8a7cf4e149ab9630783e5259d6af70a7022209e1e48fbee9b54c48535c5e")

    depends_on("c", type="build")  # generated

    depends_on("efivar")
    depends_on("popt")

    def setup_build_environment(self, env):
        env.prepend_path("CPATH", self.spec["efivar"].prefix.include.efivar)

    def install(self, spec, prefix):
        make("PREFIX={0}".format(prefix), "install")
