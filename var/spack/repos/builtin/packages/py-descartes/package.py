# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDescartes(PythonPackage):
    """Use Shapely or GeoJSON-like geometric objects as matplotlib paths
    and patches"""

    pypi = "descartes/descartes-1.1.0.tar.gz"

    version("1.1.0", sha256="135a502146af5ed6ff359975e2ebc5fa4b71b5432c355c2cafdc6dea1337035b")

    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib", type=("build", "run"))
