# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OphidiaIoServer(AutotoolsPackage):
    """In-memory IO server of the Ophidia framework"""

    homepage = "https://github.com/OphidiaBigData/ophidia-io-server"
    url = "https://github.com/OphidiaBigData/ophidia-io-server/archive/refs/tags/v1.7.3.tar.gz"
    maintainers("eldoo", "SoniaScard")
    version("1.7.3", sha256="a33f1010f72f163f103593d14e7b4480258e4c8f0094c792d2a19bcb88ef323f")
    version(
        "1.7.2",
        sha256="8b203c44e0e5497c00f1fdb2322f0b0a41f36900b62a33d95a4570ae1ccc2971",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("boost@1.79.0")
    depends_on("netcdf-c")
    depends_on("mysql")
    depends_on("bison")
    depends_on("flex")
    depends_on("ophidia-primitives")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = [
            "--with-plugin-path={0}".format(self.spec["ophidia-primitives"].prefix.lib),
            "--with-netcdf-path={0}".format(self.spec["netcdf-c"].prefix),
            "--enable-parallel-nc4",
        ]

        return args
