# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyvistaqt(PythonPackage):
    """PyQT support for PyVista."""

    homepage = "https://github.com/pyvista/pyvistaqt"
    pypi = "pyvistaqt/pyvistaqt-0.5.0.tar.gz"

    license("MIT")

    version("0.5.0", sha256="f2358825d3c5f434760c13fdff5d3681b3cf36898e6e909c8a7934a8e6448f71")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pyvista@0.25:", type=("build", "run"))
    depends_on("py-qtpy@1.9:", type=("build", "run"))
