# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchSparse(PythonPackage):
    """PyTorch Extension Library of Optimized Autograd Sparse Matrix Operations."""

    homepage = "https://github.com/rusty1s/pytorch_sparse"
    pypi = "torch-sparse/torch_sparse-0.6.18.tar.gz"
    git = "https://github.com/rusty1s/pytorch_sparse.git"

    license("MIT")
    maintainers("adamjstewart")

    version("0.6.18", sha256="2f14c510a6e93f404c6ea357210615b3c15a71731f9dbd86f25434e34fb5a741")
    version("0.6.17", sha256="06e268dd77f73eb641da8f9383306d7afac6423383c9197b9df120955e2a96bd")
    version("0.6.8", sha256="312fb5ae6e4e575fca4bbc0bd092af85e7679d5b8e53459f24492fc2a073c7b6")
    version("0.6.7", sha256="f69b2ed35baf2a9853234756a2b19e6f7ce88d2c1f029d1c7ca166d91e1adbd0")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-scipy", type=("build", "run"))

    # Undocumented dependencies
    depends_on("py-torch", type=("build", "link", "run"))
    depends_on("py-torch-scatter", type=("build", "run"))
    depends_on("parallel-hashmap", when="@0.6.17:")

    # Historical dependencies
    depends_on("py-pytest-runner", when="@:0.6.8", type="build")

    def patch(self):
        # Force build against externally-installed hashmap
        filter_file(
            "include_dirs=[extensions_dir, phmap_dir]",
            "include_dirs=[extensions_dir]",
            "setup.py",
            string=True,
        )

    def setup_build_environment(self, env):
        if self.spec.satisfies("@0.6.9:"):
            if "+cuda" in self.spec["py-torch"]:
                env.set("FORCE_CUDA", 1)
                env.set("FORCE_ONLY_CUDA", 0)
                env.set("FORCE_ONLY_CPU", 0)
            else:
                env.set("FORCE_CUDA", 0)
                env.set("FORCE_ONLY_CUDA", 0)
                env.set("FORCE_ONLY_CPU", 1)
        else:
            if "+cuda" in self.spec["py-torch"]:
                env.set("FORCE_CUDA", 1)
                env.set("FORCE_CPU", 0)
            else:
                env.set("FORCE_CUDA", 0)
                env.set("FORCE_CPU", 1)
