# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNvidiaModulus(PythonPackage):
    """A deep learning framework for AI-driven multi-physics systems."""

    homepage = "https://github.com/NVIDIA/modulus"
    url = "https://github.com/NVIDIA/modulus/archive/refs/tags/v0.5.0.tar.gz"

    license("Apache-2.0")

    version("0.5.0", sha256="ff2c7d47227b8cba59b075cac89599f8c1ec7cde60fd2db6e6874d0143828832")

    with default_args(type="build"):
        depends_on("py-setuptools")
        depends_on("py-setuptools-scm")

    with default_args(type=("build", "run")):
        depends_on("py-torch@2.0.0:")
        # Remove upper bound on numpy version
        # https://github.com/NVIDIA/modulus/issues/383
        depends_on("py-numpy@1.22.4:")
        depends_on("py-xarray@2023.1.0:")
        depends_on("py-zarr@2.14.2:")
        depends_on("py-fsspec@2023.1.0:")
        depends_on("py-s3fs@2023.5.0:")
        depends_on("py-nvidia-dali@1.16.0:")
        depends_on("py-setuptools@67.6.0:")
        depends_on("py-certifi@2023.7.22:")
        depends_on("py-pytz@2023.3:")
        depends_on("py-treelib@1.2.5:")
        depends_on("py-tqdm@4.60.0:")
        depends_on("py-nvtx@0.2.8:")
