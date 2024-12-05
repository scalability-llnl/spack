# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyUnyt(PythonPackage):
    """A package for handling numpy arrays with units."""

    homepage = "https://yt-project.org"
    pypi = "unyt/unyt-2.8.0.tar.gz"
    git = "https://github.com/yt-project/unyt.git"

    maintainers("charmoniumq")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("2.9.2", sha256="8d4bf3dd3f7b4c29580728c0359caa17d62239673eeab436448d0777adeee5e1")

    # Undocumented in 2.9.2
    depends_on("py-setuptools", type="build")

    # https://github.com/yt-project/unyt/blob/v2.9.2/setup.py#L50
    depends_on("python@3.8:", type=("build", "run"))

    # https://github.com/yt-project/unyt/blob/v2.9.2/setup.py#L21
    depends_on("py-numpy@1.17.5:", type=("build", "run"))
    depends_on("py-sympy@1.5:", type=("build", "run"))
