# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastcluster(PythonPackage):
    """Fast hierarchical clustering routines for R and Python."""

    homepage = "https://danifold.net/"
    pypi = "fastcluster/fastcluster-1.1.26.tar.gz"

    license("BSD-2-Clause")

    version("1.1.26", sha256="a202f44a3b06f5cf9cdba3c67d6c523288922d6e6a1cdf737292f93759aa82f7")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.9:", type=("build", "run"))
