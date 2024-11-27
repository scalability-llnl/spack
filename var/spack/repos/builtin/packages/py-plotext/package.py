# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPlotext(PythonPackage):
    """Plotext plots directly on terminal."""

    pypi = "plotext/plotext-5.2.8.tar.gz"
    git = "https://github.com/piccolomo/plotext.git"

    license("MIT")

    version("master", branch="master")
    version("5.2.8", sha256="319a287baabeb8576a711995f973a2eba631c887aa6b0f33ab016f12c50ffebe")

    # build dependencies
    depends_on("python@3.5.0:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
