# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeomdl(PythonPackage):
    """Object-oriented pure Python B-Spline and NURBS library."""

    homepage = "https://pypi.org/project/geomdl"
    pypi = "geomdl/geomdl-5.3.1.tar.gz"

    license("MIT")

    version("5.3.1", sha256="e81a31b4d5f111267b16045ba1d9539235a98b2cff5e4bad18f7ddcd4cb804c8")

    depends_on("py-setuptools@40.6.3:", type="build")

    # For compiling geomdl.core module
    depends_on("py-cython@:2", type="build")

    variant("viz", default=False, description="Add viz dependencies")

    depends_on("py-numpy@1.15.4:", type="run", when="+viz")
    depends_on("py-matplotlib@2.2.3:", type="run", when="+viz")
    depends_on("py-plotly", type="run", when="+viz")
