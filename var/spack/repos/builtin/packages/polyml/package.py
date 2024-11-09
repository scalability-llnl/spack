# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Polyml(AutotoolsPackage):
    """The Poly/ML implementation of Standard ML."""

    homepage = "https://polyml.org/"
    url = "https://github.com/polyml/polyml/archive/refs/tags/v5.9.1.tar.gz"

    license("LGPL-2.1-only", checked_by="draenog")

    version("5.9.1", sha256="52f56a57a4f308f79446d479e744312195b298aa65181893bce2dfc023a3663c")

    variant(
        "gmp", default=True, description="Use the GMP library for arbitrary precision arithmetic"
    )
    depends_on("gmp", when="+gmp")

    filter_compiler_wrappers("polyc", relative_root="bin")

    def configure_args(self):
        config_args = self.with_or_without("gmp")
        return config_args
