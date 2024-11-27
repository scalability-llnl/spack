# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAxPlatform(PythonPackage):
    """Adaptive experimentation is the machine-learning guided process of
    iteratively exploring a (possibly infinite) parameter space in order to identify
    optimal configurations in a resource-efficient manner. Ax currently supports
    Bayesian optimization and bandit optimization as exploration strategies. Bayesian
    optimization in Ax is powered by BoTorch, a modern library for Bayesian
    optimization research built on PyTorch."""

    homepage = "https://github.com/facebook/Ax"
    pypi = "ax-platform/ax-platform-0.3.1.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("0.3.1", sha256="0bad1d16155560fdd8644308d2771edf7fd977ad41fea15a7ecf3f224bc36517")

    depends_on("py-setuptools@34.4:", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-botorch@0.8.3:", type=("build", "run"))
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-ipywidgets", type=("build", "run"))
    depends_on("py-typeguard@2.13.3", type=("build", "run"))
    depends_on("py-plotly@5.12.0:", type=("build", "run"))

    def setup_build_environment(self, env):
        env.set("ALLOW_BOTORCH_LATEST", True)
