# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHist(PythonPackage):
    """Hist classes and utilities"""

    homepage = "https://github.com/scikit-hep/hist"
    pypi = "hist/hist-2.5.2.tar.gz"

    license("BSD-3-Clause")

    version("2.6.1", sha256="ee9034795fd2feefed923461aaccaf76f87c1f8d5414b1e704faa293ceb4fc27")
    version("2.5.2", sha256="0bafb8b956cc041f1b26e8f5663fb8d3b8f7673f56336facb84d8cfdc30ae2cf")

    variant("plot", default=False, description="Add support for drawing histograms")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@45:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")
    depends_on("py-boost-histogram@1.2.0:1.2", when="@2.5.2", type=("build", "run"))
    depends_on("py-boost-histogram@1.3.1:1.3", when="@2.6.1", type=("build", "run"))
    depends_on("py-histoprint@2.2.0:", type=("build", "run"))
    depends_on("py-numpy@1.14.5:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7:", when="^python@:3.7", type=("build", "run"))

    depends_on("py-matplotlib@3.0:", when="+plot", type=("build", "run"))
    depends_on("py-scipy@1.4:", when="+plot", type=("build", "run"))
    depends_on("py-iminuit@2:", when="+plot", type=("build", "run"))
    depends_on("py-mplhep@0.2.16:", when="+plot", type=("build", "run"))
