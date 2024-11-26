# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArt(PythonPackage):
    """ASCII art library for Python."""

    homepage = "https://www.ascii-art.site"
    pypi = "art/art-6.1.tar.gz"

    license("MIT")

    version("6.1", sha256="6ab3031e3b7710039e73497b0e750cadfe04d4c1279ce3a123500dbafb9e1b64")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
