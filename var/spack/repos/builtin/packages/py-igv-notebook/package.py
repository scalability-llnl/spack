# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyIgvNotebook(PythonPackage):
    """Module for embedding igv.js in an IPython notebook"""

    homepage = "https://github.com/igvteam/igv-notebook"
    pypi = "igv-notebook/igv-notebook-0.5.2.tar.gz"

    license("MIT license", checked_by="ashim-mahara")

    version("0.5.2", sha256="8b47a1a6c41f11359a07264815401cc4000c99722c77cbb749182bf6b66cf69c")

    depends_on("py-setuptools", type="build")

    depends_on("py-ipykernel", type=("build", "run"))
    depends_on("py-ipython", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
