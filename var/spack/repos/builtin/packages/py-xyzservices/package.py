# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXyzservices(PythonPackage):
    """xyzservices is a lightweight library providing a repository of
    available XYZ services offering raster basemap tiles."""

    homepage = "https://github.com/geopandas/xyzservices"
    pypi = "xyzservices/xyzservices-2023.10.1.tar.gz"

    license("BSD-3-Clause")

    version("2023.10.1", sha256="091229269043bc8258042edbedad4fcb44684b0473ede027b5672ad40dc9fa02")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
