# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDhScikitOptimize(PythonPackage):
    """A Modified version of scikit-optimize a Sequential model-based
    optimization toolbox for DeepHyper.
    Scikit-Optimize, or skopt, is a simple and efficient library to
    minimize (very) expensive and noisy black-box functions. It implements
    several methods for sequential model-based optimization. skopt aims to
    be accessible and easy to use in many contexts.

    The library is built on top of NumPy, SciPy and Scikit-Learn."""

    maintainers("Kerilk")

    homepage = "https://github.com/deephyper/scikit-optimize"
    pypi = "dh-scikit-optimize/dh-scikit-optimize-0.9.0.tar.gz"

    license("BSD-3-Clause")

    version("0.9.5", sha256="c2777839a536215ab40fc5db2242809ccffd5e5b23718e23d58ea76ff35a7543")
    version("0.9.4", sha256="9acfba4077fe45f3854a4af255763a3e8a396c05bd2a7c761a969171366b3840")
    version("0.9.3", sha256="0c922c61dc1f010c7bbd2f0930c766e8ae040c35b129e4de6d51b611fd72b7c9")
    version("0.9.2", sha256="9fd2d3accad7c3aca1d0edd0c88ec5490e9bc7a07f31d88f4051466a132dfd1d")
    version("0.9.1", sha256="70e70011f4fd107082174c557de70ba37c215e71a676788234b85d5c370fd7bd")
    version("0.9.0", sha256="fe70aa57ec5150a3d356b2184f0dda1ecc4ecb7e82d35edac3980094d409d676")

    variant("plots", default=False, description="Build with plot support from py-matplotlib")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-joblib@0.11:", type=("build", "run"))
    depends_on("py-pyaml@16.9:", type=("build", "run"))
    depends_on("py-numpy@1.13.3:", type=("build", "run"))
    depends_on("py-scipy@0.19.1:", type=("build", "run"))
    depends_on("py-scikit-learn@0.20.0:", type=("build", "run"))
    depends_on("py-configspace@0.4.20:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"), when="@0.9.1:")

    depends_on("py-matplotlib@2.0.0:", when="+plots", type="run")
