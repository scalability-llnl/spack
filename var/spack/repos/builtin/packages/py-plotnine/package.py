# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPlotnine(PythonPackage):
    """plotnine is an implementation of a grammar of graphics in Python, it is
    based on ggplot2. The grammar allows users to compose plots by explicitly
    mapping data to the visual objects that make up the plot."""

    homepage = "https://plotnine.readthedocs.io/en/stable"
    pypi = "plotnine/plotnine-0.8.0.tar.gz"

    license("BSD-3-Clause")

    version("0.9.0", sha256="0e89a93015f3c71d6844ac7aa9fb0da09b908f5f7dfa7dd5d68a5ca32b2ebcea")
    version("0.8.0", sha256="39de59edcc28106761b65238647d0b1f6212ea7f3a78f8be0b846616db969276")
    version("0.7.1", sha256="02f2b0435dae2e917198c5367fd97b010445d64d9888c6b7e755d3cdfe7ad057")
    version("0.7.0", sha256="8ee67cbf010ccea32670760e930b7b02177030a89ccdf85e35d156a96ce36cd3")
    version("0.6.0", sha256="aae2c8164abb209ef4f28cab01132d23f6879fcf8d492657487359e1241459e5")

    depends_on("python@3.8:", type=("build", "run"), when="@0.9.0:")
    depends_on("python@3.6:", type=("build", "run"), when="@0.6.0:")

    depends_on("py-setuptools@59:", type="build", when="@0.9.0:")
    depends_on("py-setuptools", type="build", when="@0.6.0:")

    depends_on("py-setuptools-scm@6.4:+toml", type="build", when="@0.9.0:")

    depends_on("py-descartes@1.1.0:", type=("build", "run"), when="@:0.8.0")

    depends_on("py-matplotlib@3.5.0:", type=("build", "run"), when="@0.9.0:")
    depends_on("py-matplotlib@3.1.1:", type=("build", "run"), when="@0.6.0:")

    depends_on("py-mizani@0.7.3:", type=("build", "run"), when="@0.8.0:")
    depends_on("py-mizani@0.6.0:", type=("build", "run"), when="@0.6.0:")

    depends_on("py-numpy@1.19.0:", type=("build", "run"), when="@0.8.0:")
    depends_on("py-numpy@1.16.0:", type=("build", "run"), when="@0.6.0:")

    depends_on("py-pandas@1.3.5:", type=("build", "run"), when="@0.9.0:")
    depends_on("py-pandas@1.1.0:", type=("build", "run"), when="@0.7.1:")
    depends_on("py-pandas@1.0.3:", type=("build", "run"), when="@0.7.0:")
    depends_on("py-pandas@0.25.0:", type=("build", "run"), when="@0.6.0:")

    depends_on("py-patsy@0.5.1:", type=("build", "run"), when="@0.7.0:")
    depends_on("py-patsy@0.4.1:", type=("build", "run"), when="@0.6.0:")

    depends_on("py-scipy@1.5.0:", type=("build", "run"), when="@0.8.0:")
    depends_on("py-scipy@1.2.0:", type=("build", "run"), when="@0.6.0:")

    depends_on("py-statsmodels@0.13.2:", type=("build", "run"), when="@0.9.0:")
    depends_on("py-statsmodels@0.12.1:", type=("build", "run"), when="@0.8.0:")
    depends_on("py-statsmodels@0.11.1:", type=("build", "run"), when="@0.7.0:")
    depends_on("py-statsmodels@0.9.0:", type=("build", "run"), when="@0.6.0:")
