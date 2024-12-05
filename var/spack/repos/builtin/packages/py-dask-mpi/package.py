# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDaskMpi(PythonPackage):
    """Deploying Dask using MPI4Py."""

    homepage = "https://github.com/dask/dask-mpi"
    pypi = "dask-mpi/dask-mpi-2.21.0.tar.gz"

    skip_modules = ["dask_mpi.tests"]

    license("BSD-3-Clause")

    version("2022.4.0", sha256="0a04f1d7d35a06cdff506593330d4414ea242c9172498ce191f5742eac499e17")
    version("2.21.0", sha256="76e153fc8c58047d898970b33ede0ab1990bd4e69cc130c6627a96f11b12a1a7")
    version("2.0.0", sha256="774cd2d69e5f7154e1fa133c22498062edd31507ffa2ea19f4ab4d8975c27bc3")

    depends_on("py-setuptools", type="build")

    depends_on("py-dask@2.2:", when="@:2.21.0", type=("build", "run"))
    depends_on("py-dask@2.19:", when="@2022.4.0:", type=("build", "run"))
    depends_on("py-distributed@2.19:", when="@2022.4.0:", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-mpi4py@3.0.3:", when="@2022.4.0:", type=("build", "run"))

    # jupyter-server-proxy is not a needed dependency; https://github.com/dask/dask-mpi/pull/102
    # this significantly reduces the dependency tree of py-dask-mpi
    patch("remove-dependency-jupyter-proxy.patch", when="@:2022.4.0")
