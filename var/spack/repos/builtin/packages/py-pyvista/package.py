# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyvista(PythonPackage):
    """Easier Pythonic interface to VTK."""

    homepage = "https://github.com/pyvista/pyvista"
    pypi = "pyvista/pyvista-0.32.1.tar.gz"

    # Requires optional trame dependency
    skip_modules = ["pyvista.ext", "pyvista.jupyter", "pyvista.trame"]

    maintainers("banesullivan")

    license("MIT")

    version("0.44.1", sha256="63976f5d57d151b3f7e1616dde40dcf56a66d1f37f6db067087fa9cc9667f512")
    version("0.42.3", sha256="00159cf0dea05c1ecfd1695c8c6ccfcfff71b0744c9997fc0276e661dc052351")
    version("0.37.0", sha256="d36a2c6d5f53f473ab6a9241669693acee7a5179394dc97595da14cc1de23141")
    version("0.32.1", sha256="585ac79524e351924730aff9b7207d6c5ac4175dbb5d33f7a9a2de22ae53dbf9")

    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib@3.0.1:", when="@0.39:", type=("build", "run"))
    depends_on("py-numpy@1.21:", when="@0.44:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    # https://github.com/pyvista/pyvista/releases/tag/v0.44.0
    depends_on("py-numpy@:1", when="@:0.43", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("py-pooch", when="@0.37:", type=("build", "run"))
    depends_on("py-scooby@0.5.1:", type=("build", "run"))
    depends_on("vtk+python", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))

    # Historical dependencies
    depends_on("py-appdirs", when="@:0.36", type=("build", "run"))
    depends_on("py-imageio", when="@:0.38", type=("build", "run"))
    depends_on("py-meshio@4.0.3:4", when="@:0.32", type=("build", "run"))

    # '>=3.7.*' in python_requires: setuptools parser changed in v60 and errors.
    depends_on("py-setuptools@:59", when="@:0.37", type="build")
