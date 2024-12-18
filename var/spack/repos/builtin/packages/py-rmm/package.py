# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRmm(PythonPackage):
    """RMM: RAPIDS Memory Manager. Achieving optimal
    performance in GPU-centric workflows frequently requires
    customizing how host and device memory are allocated."""

    homepage = "https://github.com/rapidsai/rmm"
    url = "https://github.com/rapidsai/rmm/archive/v0.15.0.tar.gz"

    license("Apache-2.0")

    version("0.15.0", sha256="599f97b95d169a90d11296814763f7e151a8a1e060ba10bc6c8f4684a5cd7972")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-numba", type=("build", "run"))

    for v in ("@0.15.0",):
        depends_on("librmm" + v, when=v)

    depends_on("cuda@9:")
    depends_on("spdlog")

    build_directory = "python"
