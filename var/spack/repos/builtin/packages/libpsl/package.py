# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpsl(AutotoolsPackage):
    """libpsl - C library to handle the Public Suffix List."""

    homepage = "https://github.com/rockdaboot/libpsl"
    url = "https://github.com/rockdaboot/libpsl/releases/download/0.21.2/libpsl-0.21.2.tar.gz"
    list_url = "https://github.com/rockdaboot/libpsl/tags"

    license("MIT")

    version("0.21.5", sha256="1dcc9ceae8b128f3c0b3f654decd0e1e891afc6ff81098f227ef260449dae208")
    version("0.21.2", sha256="e35991b6e17001afa2c0ca3b10c357650602b92596209b7492802f3768a6285f")
    version("0.20.2", sha256="7aa949fd3fdba61b0dc7b3f4c2520263b942c189746e157f48436386eca3398e")
    version("0.19.1", sha256="9b47387a087bcac2af31ea0c94f644bfa32e0be6d079bfa430452b7521ad8c57")
    version("0.18.0", sha256="f79c6b257dd39e8f37c7e18d293bbfa35f38676f5d6b6e918687d1cd08216439")
    version("0.17.0", sha256="025729d6a26ffd53cb54b4d86196f62c01d1813a4360c627546c6eb60ce3dd4b")

    depends_on("c", type="build")  # generated

    depends_on("icu4c")

    depends_on("gettext", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("python@2.7:", type="build")

    depends_on("valgrind~mpi~boost", type="test")

    def url_for_version(self, version):
        if version >= Version("0.21.1"):
            return super().url_for_version(version)
        url_fmt = (
            "https://github.com/rockdaboot/libpsl/releases/download/libpsl-{0}/libpsl-{0}.tar.gz"
        )
        return url_fmt.format(version)

    def configure_args(self):
        spec = self.spec

        args = [f"PYTHON={spec['python'].command.path}"]

        if self.run_tests:
            args.append("--enable-valgrind-tests")
        else:
            args.append("--disable-valgrind-tests")

        return args
