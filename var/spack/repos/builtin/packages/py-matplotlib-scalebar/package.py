# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMatplotlibScalebar(PythonPackage):
    """Provides a new artist for matplotlib to display a scale bar,
    aka micron bar."""

    homepage = "https://github.com/ppinard/matplotlib-scalebar"
    pypi = "matplotlib-scalebar/matplotlib-scalebar-0.6.1.tar.gz"
    git = "https://github.com/ppinard/matplotlib-scalebar.git"

    license("BSD-2-Clause")

    version("master", branch="master")
    version("0.8.1", sha256="14887af1093579c5e6afae51a0a1ecc3f715cdbc5c4d7ef59cdeec76ee6bb15d")
    version("0.6.1", sha256="85cec2bacf85aaf00a70cafa5786f7e66e7c0f6e9dc5c894fd6d1afaa7264ecd")

    depends_on("py-setuptools", type="build")

    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
