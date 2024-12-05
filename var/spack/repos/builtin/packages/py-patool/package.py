# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPatool(PythonPackage):
    """portable archive file manager"""

    homepage = "https://wummel.github.io/patool/"
    pypi = "patool/patool-1.12.tar.gz"

    license("GPL-3.0-or-later")

    version("1.12", sha256="e3180cf8bfe13bedbcf6f5628452fca0c2c84a3b5ae8c2d3f55720ea04cb1097")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
