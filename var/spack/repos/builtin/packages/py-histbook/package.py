# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHistbook(PythonPackage):
    """Versatile, high-performance histogram toolkit for Numpy."""

    homepage = "https://github.com/scikit-hep/histbook"
    pypi = "histbook/histbook-1.2.5.tar.gz"

    license("BSD-3-Clause")

    version("1.2.5", sha256="76d1f143f8abccf5539029fbef8133db84f377fc7752ac9e7e6d19ac9a277967")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.8.0:", type=("build", "run"))
