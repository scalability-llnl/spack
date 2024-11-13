# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStratify(PythonPackage):
    """Vectorized interpolators that are especially useful for
    Nd vertical interpolation/stratification of atmospheric and
    oceanographic datasets.
    """

    homepage = "https://github.com/SciTools-incubator/python-stratify"
    pypi = "stratify/stratify-0.1.tar.gz"

    license("BSD-3-Clause")

    version("0.1", sha256="5426f3b66e45e1010952d426e5a7be42cd45fe65f1cd73a98fee1eb7c110c6ee")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-cython", type=("build", "run"))
