# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ape(Package):
    """A tool for generating atomic pseudopotentials within a Density-Functional
    Theory framework"""

    homepage = "https://www.tddft.org/programs/APE/"
    url = "https://gitlab.com/ape/ape/-/archive/2.2.1/ape-2.2.1.tar.gz"

    version("2.2.1", sha256="3f5125182e308ab49338cad791e175ce158526a56c6ca88ac6582c1e5d7435d4")

    depends_on("gsl")
    depends_on("libxc@:4", when="@2.3.0:")
    depends_on("libxc@:2.2.2", when="@:2.2.1")

    def install(self, spec, prefix):
        args = []
        args.extend(
            [
                f"--prefix={prefix}",
                f"--with-gsl-prefix={spec['gsl'].prefix}",
                f"--with-libxc-prefix={spec['libxc'].prefix}",
            ]
        )

        # When preprocessor expands macros (i.e. CFLAGS) defined as quoted
        # strings the result may be > 132 chars and is terminated.
        # This will look to a compiler as an Unterminated character constant
        # and produce Line truncated errors. To overcome this, add flags to
        # let compiler know that the entire line is meaningful.
        # TODO: For the lack of better approach, assume that clang is mixed
        # TODO: with GNU fortran.
        if spec.satisfies("%apple-clang") or spec.satisfies("%clang") or spec.satisfies("%gcc"):
            args.extend(["FCFLAGS=-O2 -ffree-line-length-none"])

        configure(*args)
        make()
        make("install")
