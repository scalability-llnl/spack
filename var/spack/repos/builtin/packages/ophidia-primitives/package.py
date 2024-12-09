# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OphidiaPrimitives(AutotoolsPackage):
    """Array-based primitives for the Ophidia framework"""

    homepage = "https://github.com/OphidiaBigData/ophidia-primitives"
    url = "https://github.com/OphidiaBigData/ophidia-primitives/archive/refs/tags/v1.7.1.tar.gz"
    maintainers("eldoo", "SoniaScard")
    version("1.7.1", sha256="efec5248dca8fb766abcd536344eefbe2e970fb551f03454a968e59e2df69116")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("boost@1.79.0")
    depends_on("mysql")
    depends_on("libmatheval")
    depends_on("zlib-api")
    depends_on("gsl")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = ["--with-matheval-path={0}".format(self.spec["libmatheval"].prefix.lib)]

        return args
