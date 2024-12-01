# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyrr(PythonPackage):
    """3D mathematical functions using NumPy."""

    homepage = "https://github.com/adamlwgriffiths/Pyrr"
    pypi = "pyrr/pyrr-0.10.3.tar.gz"
    maintainers("JeromeDuboisPro")

    license("Unlicense")

    version("0.10.3", sha256="3c0f7b20326e71f706a610d58f2190fff73af01eef60c19cb188b186f0ec7e1d")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-multipledispatch", type=("build", "run"))
