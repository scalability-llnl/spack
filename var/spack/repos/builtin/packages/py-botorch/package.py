# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBotorch(PythonPackage):
    """BoTorch is a library for Bayesian Optimization built on PyTorch."""

    homepage = "https://botorch.org/"
    pypi = "botorch/botorch-0.6.4.tar.gz"

    maintainers("adamjstewart", "meyersbs")

    license("MIT")

    version("0.8.4", sha256="e2c17efa8fcda3c9353bbd14ba283ddf237d66151097c0af483bbaaaac61288b")
    version("0.8.3", sha256="e529f7adbb2b54f46125ae904682fc0f0d02ab8bdb9067ede521c379b355bf73")
    version("0.6.4", sha256="3fd28417f55749501a45378f72cd5ca7614e2e05b7b65c6b4eb9b72378bc665a")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("python@3.8:", when="@0.8.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@:47", when="@:0.6.4", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-setuptools-scm+toml", when="@0.8.3:", type="build")
    depends_on("py-torch@1.12:", when="@0.8.3:", type=("build", "run"))
    depends_on("py-torch@1.9:", type=("build", "run"))
    depends_on("py-gpytorch@1.10:", when="@0.8.4:", type=("build", "run"))
    depends_on("py-gpytorch@1.9.1:", when="@0.8.3:", type=("build", "run"))
    depends_on("py-gpytorch@1.6:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-multipledispatch", type=("build", "run"))
    depends_on("py-pyro-ppl@1.8.4:", when="@0.8.3:", type=("build", "run"))
    depends_on("py-pyro-ppl@1.8.0", when="@:0.6.4", type=("build", "run"))
    depends_on("py-linear-operator@0.4.0:", when="@0.8.4:", type=("build", "run"))
    depends_on("py-linear-operator@0.3.0:", when="@0.8.3:", type=("build", "run"))

    def setup_build_environment(self, env):
        if self.spec.satisfies("@0.8.3:"):
            env.set("ALLOW_LATEST_GPYTORCH_LINOP", True)
