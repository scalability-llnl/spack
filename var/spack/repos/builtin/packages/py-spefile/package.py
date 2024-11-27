# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpefile(PythonPackage):
    """Reader for SPE files part of pyspec a set of python routines for data
    analysis of x-ray scattering experiments"""

    homepage = "https://github.com/conda-forge/spefile-feedstock"
    git = "https://github.com/conda-forge/spefile-feedstock.git"

    license("BSD-3-Clause")

    version("1.6", commit="24394e066da8dee5e7608f556ca0203c9db217f9")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))

    build_directory = "recipe/src"
