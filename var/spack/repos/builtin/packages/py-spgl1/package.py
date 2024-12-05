# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpgl1(PythonPackage):
    """SPGL1 is a solver for large-scale one-norm regularized least squares.  It is
    designed to solve any of the following three problems: Basis pursuit denoise
    (BPDN): minimize ||x||_1 subject to ||Ax - b||_2 <= sigma, Basis pursuit (BP):
    minimize ||x||_1 subject to Ax = b Lasso: minimize ||Ax - b||_2 subject to
    ||x||_1 <= tau, The matrix A can be defined explicitly, or as an operator that
    returns both both Ax and A'b.  SPGL1 can solve these three problems in both
    the real and complex domains."""

    pypi = "spgl1/spgl1-0.0.2.tar.gz"
    git = "https://github.com/drrelyea/spgl1.git"

    maintainers("archxlith")

    license("LGPL-2.1-or-later")

    version("master", branch="master")
    version("0.0.2", sha256="a2a524724097bad18dd88a306dbcc99124c6c46ffcbb1a96d6ba6dd6fe2f7404")
    version("0.0.1", sha256="24ff37ab5be57f0ccf14c53090b171e019c3c12799c80f368e628e1cc9ac9a1f")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-numpy@1.15:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-setuptools", type="build")
