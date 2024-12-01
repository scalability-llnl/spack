# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROligoclasses(RPackage):
    """Classes for high-throughput arrays supported by oligo and crlmm.

    This package contains class definitions, validity checks, and
    initialization methods for classes used by the oligo and crlmm
    packages."""

    bioc = "oligoClasses"

    version("1.62.0", commit="2de6126d2a98f78d6dc80ffeef8bc76782a6dbdf")
    version("1.60.0", commit="cf9d76c2551ad061d8b882ff1dc0a5cadc64a8a7")
    version("1.58.0", commit="5544e937913bb0df54c66d738d279c38efeb30cd")
    version("1.56.0", commit="6e6c7b4ba54095d1d3c44c081839f57af9261cbf")
    version("1.52.0", commit="7995efbd2d26b8fa950830d62db92bdaf5cbeeea")
    version("1.46.0", commit="325684f66fc92f778098f24bcfbef0ce3da9717c")
    version("1.44.0", commit="d3e1134cdbea5f95b83215dc66e5f7b6a1cd0638")
    version("1.42.0", commit="ef125700d487b470281a9c1e985390633c4dd2bd")
    version("1.40.0", commit="32f40617e62d05c457baaebc7e27585b852848ed")
    version("1.38.0", commit="fe2bb7f02c7ed3cbd338254c27ceba6ff829a962")

    depends_on("r@2.14:", type=("build", "run"))
    depends_on("r-biocgenerics@0.3.2:", type=("build", "run"))
    depends_on("r-biocgenerics@0.27.1:", type=("build", "run"), when="@1.44.0:")
    depends_on("r-biobase@2.17.8:", type=("build", "run"))
    depends_on("r-iranges@2.5.17:", type=("build", "run"))
    depends_on("r-genomicranges@1.23.7:", type=("build", "run"))
    depends_on("r-summarizedexperiment", type=("build", "run"))
    depends_on("r-biostrings@2.23.6:", type=("build", "run"))
    depends_on("r-affyio@1.23.2:", type=("build", "run"))
    depends_on("r-foreach", type=("build", "run"))
    depends_on("r-biocmanager", type=("build", "run"), when="@1.44.0:")
    depends_on("r-s4vectors@0.9.25:", type=("build", "run"))
    depends_on("r-rsqlite", type=("build", "run"))
    depends_on("r-dbi", type=("build", "run"), when="@1.40.0:")
    depends_on("r-ff", type=("build", "run"))

    depends_on("r-biocinstaller", type=("build", "run"), when="@:1.42.0")
