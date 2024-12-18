# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpc(AutotoolsPackage, GNUMirrorPackage):
    """Gnu Mpc is a C library for the arithmetic of complex numbers
    with arbitrarily high precision and correct rounding of the
    result."""

    homepage = "https://www.multiprecision.org"
    gnu_mirror_path = "mpc/mpc-1.1.0.tar.gz"
    list_url = "http://www.multiprecision.org/mpc/download.html"

    license("GPL-2.0-or-later")

    version("1.3.1", sha256="ab642492f5cf882b74aa0cb730cd410a81edcdbec895183ce930e706c1c759b8")
    version("1.2.1", sha256="17503d2c395dfcf106b622dc142683c1199431d095367c6aacba6eec30340459")
    version("1.1.0", sha256="6985c538143c1208dcb1ac42cedad6ff52e267b47e5f970183a3e75125b43c2e")
    version("1.0.3", sha256="617decc6ea09889fb08ede330917a00b16809b8db88c29c31bfbb49cbf88ecc3")
    version("1.0.2", sha256="b561f54d8a479cee3bc891ee52735f18ff86712ba30f036f8b8537bae380c488")

    depends_on("c", type="build")  # generated

    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )

    # Could also be built against mpir instead
    depends_on("gmp@4.3.2:")
    depends_on("gmp@5.0.0:", when="@1.1.0:")
    depends_on("mpfr@2.4.2:")
    depends_on("mpfr@3.0.0:", when="@1.1.0:")
    depends_on("mpfr@4.1.0:", when="@1.2.1:")

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-mpfr={0}".format(spec["mpfr"].prefix),
            "--with-gmp={0}".format(spec["gmp"].prefix),
        ]
        args += self.enable_or_disable("libs")
        return args
