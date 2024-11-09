# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMapboxEarcut(PythonPackage):
    """Python bindings for the C++ implementation of the Mapbox Earcut library,
    which provides very fast and quite robust triangulation of 2D polygons."""

    homepage = "https://pypi.org/project/mapbox-earcut/"
    pypi = "mapbox-earcut/mapbox_earcut-1.0.1.tar.gz"
    git = "https://github.com/skogler/mapbox_earcut_python"

    license("ISC")

    version("1.0.1", sha256="9f155e429a22e27387cfd7a6372c3a3865aafa609ad725e2c4465257f154a438")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-pybind11@2.6:2", type="build")
    depends_on("py-numpy", type=("build", "run"))
