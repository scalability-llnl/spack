# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitFmm(PythonPackage):
    """scikit-fmm is a Python extension module which implements the fast marching
    method."""

    pypi = "scikit-fmm/scikit-fmm-2019.1.30.tar.gz"
    git = "https://github.com/scikit-fmm/scikit-fmm.git"

    maintainers("archxlith")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("2019.1.30", sha256="eb64b6d8e30b8df8f8636d5fc4fd7ca6a9b05938ccd62518c80c1d9e823069dd")

    depends_on("cxx", type="build")  # generated

    depends_on("py-numpy@1.0.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
