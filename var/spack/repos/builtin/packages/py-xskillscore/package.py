# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXskillscore(PythonPackage):
    """Metrics for verifying forecasts."""

    homepage = "https://github.com/xarray-contrib/xskillscore"
    pypi = "xskillscore/xskillscore-0.0.24.tar.gz"

    license("Apache-2.0")

    version("0.0.24", sha256="ce3306c60626eafea722a1522016e272ca516ce6f2447c75f92c52888939f8c2")

    with default_args(type="build"):
        depends_on("py-setuptools-scm")
        depends_on("py-setuptools@30.3:")
        depends_on("py-setuptools-scm-git-archive")

    with default_args(type=("build", "run")):
        depends_on("py-bottleneck")
        depends_on("py-cftime")
        depends_on("py-dask")
        depends_on("py-numba@0.52:")
        depends_on("py-numpy")
        depends_on("py-properscoring")
        depends_on("py-scikit-learn")
        depends_on("py-scipy")
        depends_on("py-toolz")
        depends_on("py-xarray@0.16.1:")
        depends_on("py-xhistogram@0.3.0:")
