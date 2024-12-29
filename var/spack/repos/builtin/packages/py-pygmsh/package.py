# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygmsh(PythonPackage):
    """Easier Pythonic interface to GMSH."""

    homepage = "https://github.com/nschloe/pygmsh"
    url = "https://github.com/nschloe/pygmsh/archive/refs/tags/v7.1.17.tar.gz"

    maintainers("tech-91")

    license("GPL-3.0-only")

    version("7.1.17", sha256="9c9c0fb507eb5c0d0f1f64a23909b3bda25652df737e935ea9336b08773afc4e")

    depends_on("py-flit-core@3.2:4", type="build", when="@1.3:")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-meshio@4.3.2:6", type=("build", "run"))
    depends_on("py-gmsh", type=("build", "run"))
    depends_on("py-numpy@1.20.0:1.26.4", type=("build", "run"))
