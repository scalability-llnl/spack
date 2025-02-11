# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyCudaPython(PythonPackage):
    """Python bindings for CUDA."""

    homepage = "https://nvidia.github.io/cuda-python/"
    url = "https://github.com/NVIDIA/cuda-python/archive/refs/tags/v11.8.0.tar.gz"

    version("11.8.0", sha256="afc4f0ac46c0e734a71f97d52390424aec1bc9fceb324e30095ca09bc678ff72")

    depends_on("py-setuptools", type="build")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-future", type=("build", "run"))
    depends_on("py-pyparsing", type=("build", "run"))

    depends_on("py-cython@0.29.34", type=("build", "run"))
    depends_on("py-pytest@6.2.4:", type=("build", "run"))
    depends_on("py-pytest-benchmark@3.4.1:", type=("build", "run"))
    depends_on("py-numpy@1.21.1:", type=("build", "run"))
    depends_on("py-pyclibrary@0.1.7:", type=("build", "run"))

    depends_on("cuda@:11.8")

    def setup_build_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.spec["cuda"].prefix.lib)
