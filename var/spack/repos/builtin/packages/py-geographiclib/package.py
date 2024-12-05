# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeographiclib(PythonPackage):
    """The geodesic routines from GeographicLib."""

    homepage = "https://geographiclib.sourceforge.io/1.50/python"
    pypi = "geographiclib/geographiclib-1.50.tar.gz"

    maintainers("adamjstewart")

    license("MIT")

    version("1.50", sha256="12bd46ee7ec25b291ea139b17aa991e7ef373e21abd053949b75c0e9ca55c632")

    depends_on("py-setuptools", type="build")
