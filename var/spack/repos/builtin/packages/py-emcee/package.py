# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEmcee(PythonPackage):
    """emcee is an MIT licensed pure-Python implementation of Goodman & Weare's
    Affine Invariant Markov chain Monte Carlo (MCMC) Ensemble sampler."""

    homepage = "https://dan.iel.fm/emcee/current/"
    pypi = "emcee/emcee-2.2.1.tar.gz"

    license("MIT")

    version("3.1.1", sha256="48ffc6a7f5c51760b7a836056184c7286a9959ef81b45b977b02794f1210fb5c")
    version("3.0.2", sha256="035a44d7594fdd03efd10a522558cdfaa080e046ad75594d0bf2aec80ec35388")
    version("2.2.1", sha256="b83551e342b37311897906b3b8acf32979f4c5542e0a25786ada862d26241172")
    version("2.1.0", sha256="5ce1039a3d78fb9e7d53fcd768517585c5998193743bfcfaac407927d375ca63")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@40.6.0:", type="build", when="@3.1.1:")
    depends_on("py-setuptools-scm", type="build", when="@3.1.1:")
    depends_on("py-wheel", type="build", when="@3.1.1:")
    depends_on("py-numpy", type=("build", "run"))
