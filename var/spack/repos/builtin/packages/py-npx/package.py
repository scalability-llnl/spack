# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNpx(PythonPackage):
    """Some useful extensions for NumPy"""

    homepage = "https://github.com/nschloe/npx"
    pypi = "npx/npx-0.1.0.tar.gz"

    license("BSD-3-Clause")

    version("0.1.0", sha256="3edec9508326b6724d7c176dbcba2098508788241b8a671aab583d0c72b2f05b")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-flit-core@3.2:3", type="build")
    depends_on("py-numpy@1.20.0:", type=("build", "run"))
