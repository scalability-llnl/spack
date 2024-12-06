# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSummarizedexperiment(RPackage):
    """SummarizedExperiment container.

    The SummarizedExperiment container contains one or more assays, each
    represented by a matrix-like object of numeric or other mode. The rows
    typically represent genomic ranges of interest and the columns represent
    samples."""

    bioc = "SummarizedExperiment"

    version("1.30.0", commit="a2843fbced9fc345c9061b2e52244f3263326e2e")
    version("1.28.0", commit="ba55dac12224f0aafe8f52f1397611b5efb41626")
    version("1.26.1", commit="c8cbd3b4f0fa1d686c4d7ce5b8614a24c74b2074")
    version("1.24.0", commit="d37f19383d03c107a8a41c0df2326e28efe46b28")
    version("1.20.0", commit="874aa87a481e4076a0ec3369f55c9c0a1ab8025e")
    version("1.18.2", commit="e22fafe8c314b4e216fb130012d631b4626bc605")
    version("1.14.1", commit="2c68d99e11c7345e5ed388370822ea48395c64a4")
    version("1.12.0", commit="5f8416864636add121ec1d6737ebb89a42227fd7")
    version("1.10.1", commit="7ad2e991c8285bfc4b2e15b29d94cc86d07f8f2b")
    version("1.8.1", commit="9d8a29aa9c78bbc7dcc6472537e13fc0d11dc1f7")
    version("1.6.5", commit="ec69cd5cfbccaef148a9f6abdfb3e22e888695d0")

    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.24.0:")
    depends_on("r-matrixgenerics@1.1.3:", type=("build", "run"))
    depends_on("r-genomicranges@1.27.22:", type=("build", "run"))
    depends_on("r-genomicranges@1.29.14:", type=("build", "run"), when="@1.8.1:")
    depends_on("r-genomicranges@1.31.17:", type=("build", "run"), when="@1.10.1:")
    depends_on("r-genomicranges@1.33.6:", type=("build", "run"), when="@1.12.0:")
    depends_on("r-genomicranges@1.41.5:", type=("build", "run"), when="@1.20.0:")
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-biocgenerics@0.15.3:", type=("build", "run"))
    depends_on("r-biocgenerics@0.37.0:", type=("build", "run"), when="@1.24.0:")
    depends_on("r-s4vectors@0.13.13:", type=("build", "run"))
    depends_on("r-s4vectors@0.17.25:", type=("build", "run"), when="@1.10.1:")
    depends_on("r-s4vectors@0.27.12:", type=("build", "run"), when="@1.20.0:")
    depends_on("r-s4vectors@0.33.7:", type=("build", "run"), when="@1.26.1:")
    depends_on("r-iranges@2.7.2:", type=("build", "run"))
    depends_on("r-iranges@2.11.17:", type=("build", "run"), when="@1.8.1:")
    depends_on("r-iranges@2.13.16:", type=("build", "run"), when="@1.10.1:")
    depends_on("r-iranges@2.23.9:", type=("build", "run"), when="@1.20.0:")
    depends_on("r-genomeinfodb@1.11.4:", type=("build", "run"))
    depends_on("r-genomeinfodb@1.13.1:", type=("build", "run"), when="@1.8.1:")
    depends_on("r-delayedarray@0.1.9:", type=("build", "run"))
    depends_on("r-delayedarray@0.3.20:", type=("build", "run"), when="@1.8.1:")
    depends_on("r-delayedarray@0.15.10:", type=("build", "run"), when="@1.20.0:")
