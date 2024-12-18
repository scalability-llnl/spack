# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Unuran(AutotoolsPackage):
    """Universal Non-Uniform Random number generator."""

    homepage = "https://statmath.wu.ac.at/unuran"
    url = "https://statmath.wu.ac.at/unuran/unuran-1.8.1.tar.gz"

    license("GPL-2.0-or-later")

    version("1.8.1", sha256="c270ae96857857dbac6450043df865e0517f52856ddbe5202fd35583b13c5193")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Enable the build of shared libraries")
    variant(
        "rngstreams",
        default=True,
        description="Use RNGSTREAM library for uniform random generation",
    )
    variant(
        "gsl",
        default=False,
        description="Use random number generators from GNU Scientific Library",
    )

    depends_on("gsl", when="+gsl")
    depends_on("rngstreams", when="+rngstreams")

    def configure_args(self):
        spec = self.spec

        args = [
            "--%s-shared" % ("enable" if "+shared" in spec else "disable"),
            "--with-urgn-default=%s" % ("rngstream" if "+rngstreams" in spec else "builtin"),
            "--%s-urng-gsl" % ("with" if "+gsl" in spec else "without"),
            "--%s-urng-rngstreams" % ("with" if "+rngstreams" in spec else "without"),
        ]

        return args
