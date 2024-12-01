# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPostcactus(PythonPackage):
    """This repository contains a Python package named PostCactus for
    postprocessing data from numerical simulations performed with the Einstein
    Toolkit."""

    homepage = "https://github.com/wokast/PyCactus"
    url = "https://github.com/wokast/PyCactus/archive/refs/tags/2.2.zip"

    version("2.2", sha256="303108835d7652b37f43871c735b99dc7a60c28a24de35a09e9d2bb0f28f93fb")

    # pyproject.toml
    depends_on("py-setuptools@40.6.0:", type="build")
    # setup.cfg
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-tables", type=("build", "run"))
    depends_on("py-jupyter", type=("build", "run"), when="+jupyter")
    depends_on("vtk", type=("build", "run"), when="+vtk")

    # Variants for the optional requirements in README.md
    variant("jupyter", default=False, description="Support for jupyter")
    variant("vtk", default=False, description="VTK for 3D plots")

    def patch(self):
        # Commenting out build-backend in order to ignore a ModuleNotFoundError
        # for setuptools.build-meta
        filter_file("^build-backend", "# build-backend", "PostCactus/pyproject.toml")

    build_directory = "PostCactus"
