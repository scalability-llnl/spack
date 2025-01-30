# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Maxima(AutotoolsPackage):
    """
    Maxima is a system for the manipulation of symbolic and numerical expressions,
    including differentiation, integration, Taylor series, Laplace transforms,
    ordinary differential equations, systems of linear equations, polynomials, sets,
    lists, vectors, matrices and tensors. Maxima yields high precision numerical
    results by using exact fractions, arbitrary-precision integers and
    variable-precision floating-point numbers. Maxima can plot functions and
    data in two and three dimensions.
    """

    homepage = "https://maxima.sourceforge.io/"
    url = "https://sourceforge.net/projects/maxima/files/Maxima-source/5.47.0-source/maxima-5.47.0.tar.gz/download"
    license("BSD-3-Clause", checked_by="adaell")
    maintainers("adaell")
    version(
        "5.47.0",
        sha256="9104021b24fd53e8c03a983509cb42e937a925e8c0c85c335d7709a14fd40f7a",
    )

    depends_on("sbcl")

    def configure_args(self):
        args = ["--disable-build-docs"]
        return args

    def install(self, spec, prefix):
        make()
        make("install")
