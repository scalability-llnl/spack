# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXhistogram(PythonPackage):
    """Fast, flexible, label-aware histograms for numpy and xarray."""

    homepage = "https://github.com/xgcm/xhistogram"
    pypi = "xhistogram/xhistogram-0.3.2.tar.gz"

    license("MIT")

    version("0.3.2", sha256="56b0751e1469eaed81710f644c8ba5c574b51883baa2feee26a95f2f708f91a1")

    depends_on("py-setuptools", type="build")
    depends_on("py-xarray@0.12:", type=("build", "run"))
    depends_on("py-dask@2.3:+array", type=("build", "run"))
    depends_on("py-numpy@1.17:", type=("build", "run"))
