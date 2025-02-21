# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRanger(RPackage):
    """A Fast Implementation of Random Forests.

    A fast implementation of Random Forests, particularly suited for high
    dimensional data. Ensembles of classification, regression, survival and
    probability prediction trees are supported. Data from genome-wide
    association studies can be analyzed efficiently. In addition to data
    frames, datasets of class 'gwaa.data' (R package 'GenABEL') and 'dgCMatrix'
    (R package 'Matrix') can be directly analyzed."""

    cran = "ranger"

    license("GPL-3.0-only")

    version("0.16.0", sha256="0395f93afdb807a7882c1fa8f183a26a871c5168ea0903566951298ef1138589")
    version("0.15.1", sha256="4d65d9ee7c5f2704a0e303a27222c02aa53e49f3c28dc0b4451371e37ada2b2e")
    version("0.14.1", sha256="5d99401d555da1cfb11c70e59d1bb545ce48720073a06a2a32eb396f622dee1b")
    version("0.13.1", sha256="60934f0accc21edeefddbb4ddebfdd7cd10a3d3e90b31aa2e6e4b7f50d632d0a")
    version("0.12.1", sha256="fc308e0ac06718272799928e1a19612de16b05bde481d8f38e11a101df5425ef")
    version("0.11.2", sha256="13ac8a9433fdd92f62f66de44abc52477dcbb436b2045c1947951a266bffbeeb")
    version("0.11.1", sha256="999fb114602e27601ff0fe8ab461c39d667c6f5e8434e7feb3d21c7caf0dcffb")
    version("0.8.0", sha256="7f0fdee2f2d553a0aec56c2a4a4ff9dd972e1c7284118d9ea570749e0eaaabb9")
    version("0.7.0", sha256="83f4b06c6e63da979a20b757aaf0042928db453c12d89281afd40046e6b5393c")
    version("0.6.0", sha256="2759c2a3271098a4cfb63cd3ea68acaf645c92cb24c86fba098ada06e2e298bb")
    version("0.5.0", sha256="bc55811e723c9076c35aac4d82f29770ef84b40846198235d8b0ea9a4e91f144")
    version("0.4.0", sha256="d9f5761c3b07357aa586270cf7cbc97fc3db56ba731b6d0f3baf296f635f2be5")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r-rcpp@0.11.2:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-rcppeigen", type=("build", "run"))
