# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sollya(AutotoolsPackage):
    """Sollya is both a tool environment and a library for safe floating-point code
    development. It is particularily targeted to the automatized implementation of
    mathematical floating-point libraries (libm). Amongst other features, it offers
    a certified infinity (supremum) norm and a fast Remez algorithm."""

    homepage = "https://www.sollya.org"
    url = "https://www.sollya.org/releases/sollya-7.0/sollya-7.0.tar.bz2"

    license("LGPL-3.0-or-later")

    version("7.0", sha256="15745871f7dd3e96e12915098dd6df2078b815853a38143b2bc6c01477044984")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("gmp")
    depends_on("mpfi")
    depends_on("mpfr")
    depends_on("libxml2")
    depends_on("fplll")

    def configure_args(self):
        args = [
            "--with-gmp=" + self.spec["gmp"].prefix,
            "--with-mpfr=" + self.spec["mpfr"].prefix,
            "--with-mpfi=" + self.spec["mpfi"].prefix,
            "--with-xml2=" + self.spec["libxml2"].prefix,
            "--with-fplll=" + self.spec["fplll"].prefix,
        ]
        return args
