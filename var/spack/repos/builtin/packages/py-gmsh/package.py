# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGmsh(PythonPackage):
    """Pythonic interface to GMSH."""

    homepage = "https://pypi.org/project/gmsh"
    url = "https://files.pythonhosted.org/packages/30/cb/44245b93105e93ca0223f4dfbfd199803b10770e79dee63f63cb755570e0/gmsh-4.13.1-py2.py3-none-manylinux_2_24_x86_64.whl"

    maintainers("tech-91")

    license("GPL-2.0-or-later")

    version("4.13.1", sha256="89ab53b6ec28f099b723da35bcdb6f5df779b10a9c0e6b09e8059906c3a48b27")
    depends_on("gmsh+opencascade", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"))
