# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTidynamics(PythonPackage):
    """A tiny package to compute the dynamics of stochastic and molecular simulations."""

    homepage = "https://lab.pdebuyl.be/tidynamics/"
    pypi = "tidynamics/tidynamics-1.0.0.tar.gz"

    maintainers("RMeli")

    license("BSD-3-Clause")

    version("1.1.2", sha256="103874edd79dc64a0c7b765f51200926822e74df63703acb6c630a8167dbcfa2")
    version("1.0.0", sha256="b7bd669d380b0f469f3a8aedfbc0e5fa967fe8dc44e196f54baf0edb59846976")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", when="@1.1.2:", type="build")

    depends_on("py-numpy", type=("build", "run"))
