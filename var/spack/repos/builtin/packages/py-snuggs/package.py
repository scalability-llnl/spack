# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySnuggs(PythonPackage):
    """Snuggs are s-expressions for Numpy"""

    homepage = "https://github.com/mapbox/snuggs"
    url = "https://github.com/mapbox/snuggs/archive/1.4.1.zip"

    license("MIT")

    version("1.4.1", sha256="b37ed4e11c5f372695dc6fe66fce6cede124c90a920fe4726c970c9293b71233")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-pyparsing", type=("build", "run"))
