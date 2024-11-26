# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchScatter(PythonPackage):
    """PyTorch Extension Library of Optimized Scatter Operations."""

    homepage = "https://github.com/rusty1s/pytorch_scatter"
    pypi = "torch-scatter/torch_scatter-2.1.2.tar.gz"
    git = "https://github.com/rusty1s/pytorch_scatter.git"

    license("MIT")
    maintainers("adamjstewart")

    version("2.1.2", sha256="69b3aa435f2424ac6a1bfb6ff702da6eb73b33ca0db38fb26989c74159258e47")

    depends_on("cxx", type="build")  # generated

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")

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
