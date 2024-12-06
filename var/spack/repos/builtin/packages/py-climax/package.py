# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClimax(PythonPackage):
    """ClimaX: A foundation model for weather and climate."""

    homepage = "https://github.com/microsoft/ClimaX"
    url = "https://github.com/microsoft/ClimaX/archive/refs/tags/v0.3.1.tar.gz"
    git = "https://github.com/microsoft/ClimaX.git"

    license("MIT")

    version("main", branch="main")
    version("0.3.1", sha256="1a8ab02fd1083de4340e26889ceea75f9dbc6e56433c731ba616cb46767872fc")

    # pyproject.toml
    depends_on("py-setuptools", type="build")

    # docker/environment.yml
    # (only including deps that are actually imported, ignoring version)
    with default_args(type=("build", "run")):
        depends_on("py-click")
        depends_on("py-numpy")
        depends_on("py-pytorch-lightning")
        depends_on("py-scipy")
        depends_on("py-timm")
        depends_on("py-torch")
        depends_on("py-torchdata")
        depends_on("py-tqdm")
        depends_on("py-xarray")
        depends_on("py-xesmf")
