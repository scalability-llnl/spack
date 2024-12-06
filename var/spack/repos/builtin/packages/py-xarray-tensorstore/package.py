# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXarrayTensorstore(PythonPackage):
    """Xarray-TensorStore is a small library that allows opening Zarr arrays into Xarray
    via TensorStore, instead of the standard Zarr-Python library.
    """

    homepage = "https://github.com/google/xarray-tensorstore"
    pypi = "xarray-tensorstore/xarray-tensorstore-0.1.1.tar.gz"

    license("Apache-2.0")

    version("0.1.1", sha256="2ee6f164c9f1bc43328245b8d06c21863204fcd4e6159ddd6d8867c313c1d9b4")

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-numpy")
        depends_on("py-xarray")
        depends_on("py-zarr")
        depends_on("py-tensorstore")
