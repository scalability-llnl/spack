# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCmocean(PythonPackage):
    """Colormaps for Oceanography."""

    homepage = "https://matplotlib.org/cmocean/"
    pypi = "cmocean/cmocean-2.0.tar.gz"

    license("MIT")

    version("4.0.3", sha256="37868399fb5f41b4eac596e69803f9bfaea49946514dfb2e7f48886854250d7c")
    version("3.0.3", sha256="abaf99383c1a60f52970c86052ae6c14eafa84fc16984488040283c02db77c0b")
    version("2.0", sha256="13eea3c8994d8e303e32a2db0b3e686f6edfb41cb21e7b0e663c2b17eea9b03a")

    depends_on("python@3.8:", when="@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging", when="@3:", type=("build", "run"))

    # https://github.com/matplotlib/cmocean/pull/99
    conflicts("^py-numpy@2:", when="@:3.0")
