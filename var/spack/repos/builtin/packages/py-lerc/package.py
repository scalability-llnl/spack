# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLerc(PythonPackage):
    """Limited Error Raster Compression."""

    homepage = "https://github.com/Esri/lerc"
    pypi = "lerc/lerc-0.1.0.tar.gz"

    version("0.1.0", sha256="46cac3f5a0194518f49a52e3ae073093fc85b0d79396383b64b1f9dba4aeacc1")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
