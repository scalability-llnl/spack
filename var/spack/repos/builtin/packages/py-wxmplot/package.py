# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWxmplot(PythonPackage):
    """wxPython plotting widgets using matplotlib."""

    homepage = "https://newville.github.io/wxmplot/"
    pypi = "wxmplot/wxmplot-0.9.38.tar.gz"

    license("MIT")

    version("0.9.38", sha256="82dc64abb42bdd03ec7067a3aa2a475001f2bc8e4772149bae47facf460c0081")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.12:", type=("build", "run"))
    depends_on("py-six@1.10:", type=("build", "run"))
    depends_on("py-matplotlib@2.0:", type=("build", "run"))
    depends_on("py-wxpython@4.0.3:", type=("build", "run"))
