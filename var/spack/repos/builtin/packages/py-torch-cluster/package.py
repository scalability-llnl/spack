# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchCluster(PythonPackage):
    """PyTorch Extension Library of Optimized Graph Cluster Algorithms."""

    homepage = "https://github.com/rusty1s/pytorch_cluster"
    pypi = "torch-cluster/torch_cluster-1.6.3.tar.gz"
    git = "https://github.com/rusty1s/pytorch_cluster.git"

    license("MIT")
    maintainers("adamjstewart")

    version("1.6.3", sha256="78d5a930a5bbd0d8788df8c6d66addd68d6dd292fe3edb401e3dacba26308152")

    depends_on("cxx", type="build")  # generated

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-scipy", type=("build", "run"))

    # Undocumented dependencies
    depends_on("py-torch", type=("build", "link", "run"))

    def setup_build_environment(self, env):
        if "+cuda" in self.spec["py-torch"]:
            env.set("FORCE_CUDA", 1)
            env.set("FORCE_ONLY_CUDA", 0)
            env.set("FORCE_ONLY_CPU", 0)
        else:
            env.set("FORCE_CUDA", 0)
            env.set("FORCE_ONLY_CUDA", 0)
            env.set("FORCE_ONLY_CPU", 1)
