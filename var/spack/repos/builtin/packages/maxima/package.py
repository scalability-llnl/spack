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
    maintainers("adaell")
    license("BSD-3-Clause", checked_by="adaell")
    version(
        "5.47.0",
        sha512="953b98336eb086069edaa917981372450ce165dedd7a7b39b181d3f2d8b089551eea943e0084148eaa3ded395dcba9135509d3d11d9132ab7a3ad8bb800d3a11",
    )

    depends_on("sbcl")

    def configure_args(self):
        args = ["--disable-build-docs"]

        return args

    def install(self, spec, prefix):
        make()
        make("install")
