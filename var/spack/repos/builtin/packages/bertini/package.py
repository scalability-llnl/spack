# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bertini(AutotoolsPackage):
    """Bertini is a general-purpose solver, written in C, that was created
    for research about polynomial continuation. It solves for the numerical
    solution of systems of polynomial equations using homotopy continuation."""

    homepage = "https://bertini.nd.edu/"
    url = "https://bertini.nd.edu/BertiniSource_v1.5.tar.gz"

    license("GPL-3.0-or-later")

    version("1.5", sha256="a9a68a96e180fe6a93ba1bc1d61f522784c9a053b049b2cbd98008b5b6deec3c")

    depends_on("c", type="build")  # generated

    variant("mpi", default=True, description="Compile in parallel")

    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("gmp")
    depends_on("mpfr")
    depends_on("mpi", when="+mpi")
