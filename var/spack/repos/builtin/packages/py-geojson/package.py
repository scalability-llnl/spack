# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeojson(PythonPackage):
    """Python bindings and utilities for GeoJSON."""

    homepage = "https://github.com/jazzband/geojson"
    pypi = "geojson/geojson-3.1.0.tar.gz"

    maintainers("Chrismarsh")

    license("BSD-3-Clause", checked_by="Chrismarsh")

    version("3.2.0", sha256="b860baba1e8c6f71f8f5f6e3949a694daccf40820fa8f138b3f712bd85804903")
    version("3.1.0", sha256="58a7fa40727ea058efc28b0e9ff0099eadf6d0965e04690830208d3ef571adac")

    depends_on("python@3.7:3.12", when="@3.1.0")
    depends_on("python@3.7:3.13", when="@3.2.0")
    depends_on("py-setuptools", type="build")
