# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHist(PythonPackage):
    """Hist classes and utilities"""

    homepage = "https://github.com/scikit-hep/hist"
    pypi = "hist/hist-2.5.2.tar.gz"

    license("BSD-3-Clause")

    version("2.7.2", sha256="26b1ab810d8b10222db5d161d4acaf64aaa04fe6baaed2966d41c1dac5601d06")
    version("2.7.1", sha256="ffbe314c2bd03c342b9f168dce715ad8f36281eb23172a00970882a9344fe988")
    version("2.7.0", sha256="0ce40fd898ded8ef23d97c77cf1da9caf47b3caaef5fde190055d4d679a2d7a4")
    version("2.6.3", sha256="dede097733d50b273af9f67386e6dcccaab77e900ae702e1a9408a856e217ce9")
    version("2.6.2", sha256="55bb6366728ee48cb3fe48f20f92f0dbc560837a95961c39651699bb63af720a")
    version("2.6.1", sha256="ee9034795fd2feefed923461aaccaf76f87c1f8d5414b1e704faa293ceb4fc27")
    version("2.5.2", sha256="0bafb8b956cc041f1b26e8f5663fb8d3b8f7673f56336facb84d8cfdc30ae2cf")

    variant("plot", default=False, description="Add support for drawing histograms")
    variant("dask", default=False, description="Add support for dask histograms", when="@2.6.3:")
    variant("fit", default=False, description="Add support for fitting histograms", when="@2.7.1:")

    depends_on("python@3.7:", type=("build", "run"))
    with when("@:2.6.1"):
        depends_on("py-setuptools@45:", type="build")
        depends_on("py-setuptools-scm@3.4:+toml", type="build")
    with when("@2.6.2:"):
        depends_on("py-hatchling", type="build")
        depends_on("py-hatch-vcs", type="build")

    depends_on("py-boost-histogram@1.2.0:1.2", when="@2.5.2", type=("build", "run"))
    depends_on("py-boost-histogram@1.3.1:1.3", when="@2.6.1:2.7.1", type=("build", "run"))
    depends_on("py-boost-histogram@1.3.1:1.4", when="@2.7.2:", type=("build", "run"))
    depends_on("py-histoprint@2.2.0:", type=("build", "run"))
    depends_on("py-numpy@1.14.5:", type=("build", "run"), when="@:2.7.1")
    depends_on("py-numpy@1.14.5:", type=("build", "run"), when="@2.7.2: ^python@:3.11")
    depends_on("py-numpy@1.26:", type=("build", "run"), when="@2.7.2: ^python@3.12:")
    depends_on("py-typing-extensions@3.7:", when="@:2.6 ^python@:3.7", type=("build", "run"))
    depends_on("py-typing-extensions@4:", when="@2.7: ^python@:3.11", type=("build", "run"))

    with when("+plot"):
        depends_on("py-matplotlib@3.0:", type=("build", "run"))
        depends_on("py-mplhep@0.2.16:", type=("build", "run"))
        with when("@:2.7.0"):
            depends_on("py-scipy@1.4:", type=("build", "run"), when="@:2.6.1,2.7.0")
            depends_on("py-iminuit@2:", type=("build", "run"), when="@:2.6.1,2.7.0")
            depends_on("py-scipy@1.4:", type=("build", "run"), when="@2.6.2:2.6.3 ^python@:3.10")
            depends_on("py-iminuit@2:", type=("build", "run"), when="@2.6.2:2.6.3 ^python@:3.10")

    with when("+dask"):
        depends_on("py-dask@2022: +dataframe", type=("build", "run"), when="^python@3.8:")
        depends_on("py-dask-histogram@2023.1:", type=("build", "run"), when="^python@3.8:")

    with when("+fit"):
        depends_on("py-scipy@1.4:", type=("build", "run"))
        depends_on("py-iminuit@2:", type=("build", "run"))
