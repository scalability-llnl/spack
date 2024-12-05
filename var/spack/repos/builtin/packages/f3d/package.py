# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class F3d(CMakePackage):
    """A fast and minimalist scriptable 3D viewer."""

    homepage = "https://f3d-app.github.io"
    url = "https://github.com/f3d-app/f3d/archive/refs/tags/v1.1.1.tar.gz"

    license("BSD-3-Clause")

    version("2.0.0", sha256="5b335de78a9f68903d7023d947090d4b36fa15b9e165749906a82153e0f56d05")
    version("1.1.1", sha256="68bdbe3a90f2cd553d5e090a95d3c847e2a2f06abbe225ffecd47d3d29978b0a")

    depends_on("cxx", type="build")  # generated

    depends_on("vtk@9:", type="link")
