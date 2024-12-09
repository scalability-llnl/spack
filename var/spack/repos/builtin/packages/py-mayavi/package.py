# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMayavi(PythonPackage):
    """Mayavi: 3D visualization of scientific data in Python."""

    homepage = "https://github.com/enthought/mayavi"
    pypi = "mayavi/mayavi-4.7.3.tar.gz"

    license("EPL-1.0")

    version("4.7.3", sha256="670d0023b9cd2d2346c451db9ba2f61da23a5df5033b25aea89cb6d81b9464f0")
    version(
        "4.7.1",
        sha256="be51fb6f886f304f7c593c907e6a2e88d7919f8f446cdccfcd184fa35b3db724",
        url="https://files.pythonhosted.org/packages/source/m/mayavi/mayavi-4.7.1.tar.bz2",
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-apptools", type=("build", "run"))
    depends_on("py-envisage", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pyface@6.1.1:", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-traits@6:", when="@4.7.2:", type=("build", "run"))
    depends_on("py-traits@4.6:", type=("build", "run"))
    depends_on("py-traitsui@7:", when="@4.7.2:", type=("build", "run"))
    depends_on("py-traitsui@6:", type=("build", "run"))
    depends_on("vtk+python", type=("build", "run"))
    depends_on("py-pyqt5", type=("build", "run"))
