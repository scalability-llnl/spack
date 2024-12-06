# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpatialite(PythonPackage):
    """Wrapper for standard Python module "sqlite3" which adds SpatiaLite
    support.
    """

    homepage = "https://github.com/malexer/spatialite"
    pypi = "spatialite/spatialite-0.0.3.tar.gz"

    license("MIT")

    version("0.0.3", sha256="a0761f239a52f326b14ce41ba61b6614dfcc808b978a0bec4a37c1de9ad9071e")

    depends_on("py-setuptools", type="build")
    depends_on("libspatialite")
