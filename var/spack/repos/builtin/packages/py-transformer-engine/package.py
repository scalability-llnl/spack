# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTransformerEngine(PythonPackage):
    """
    A library for accelerating Transformer models on NVIDIA GPUs, including fp8 precision on Hopper
    GPUs.
    """

    homepage = "https://github.com/NVIDIA/TransformerEngine"
    url = "https://github.com/NVIDIA/TransformerEngine/archive/refs/tags/v0.0.tar.gz"
    git = "https://github.com/NVIDIA/TransformerEngine.git"
    maintainers("aurianer")

    license("Apache-2.0")

    version("1.4", tag="v1.4", submodules=True)
    version("main", branch="main", submodules=True)

    depends_on("cxx", type="build")  # generated

    variant("userbuffers", default=True, description="Enable userbuffers, this option needs MPI.")

    depends_on("py-setuptools", type="build")
    depends_on("cmake@3.18:")
    depends_on("py-pydantic")
    depends_on("py-importlib-metadata")

    with default_args(type=("build", "run")):
        depends_on("py-accelerate")
        depends_on("py-datasets")
        depends_on("py-flash-attn@2.2:2.4.2")
        depends_on("py-packaging")
        depends_on("py-torchvision")
        depends_on("py-transformers")
        depends_on("mpi", when="+userbuffers")

    with default_args(type=("build", "link", "run")):
        depends_on("py-torch+cuda+cudnn")

    def setup_build_environment(self, env):
        env.set("NVTE_FRAMEWORK", "pytorch")
        if self.spec.satisfies("+userbuffers"):
            env.set("NVTE_WITH_USERBUFFERS", "1")
            env.set("MPI_HOME", self.spec["mpi"].prefix)
