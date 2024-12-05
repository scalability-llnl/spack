# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGmshInterop(PythonPackage):
    """Interoperability between Python and Gmsh"""

    homepage = "https://documen.tician.de/gmsh_interop"
    pypi = "gmsh_interop/gmsh_interop-2021.1.1.tar.gz"
    git = "https://github.com/inducer/gmsh_interop.git"

    maintainers("cgcgcg")

    license("MIT")

    version("2021.1.1", sha256="5456903283327dfa57fd973bb463c5fbc1c98c8f7ad15327441acb75da10b5f1")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.6:", type=("build", "run"))
    depends_on("py-pytools", type=("build", "run"))
