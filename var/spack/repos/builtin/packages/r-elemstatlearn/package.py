# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RElemstatlearn(RPackage):
    """Data Sets, Functions and Examples from the Book: "The Elements of
    Statistical Learning, Data Mining, Inference, and Prediction" by Trevor
    Hastie, Robert Tibshirani and Jerome Friedman"""

    cran = "ElemStatLearn"

    version(
        "2015.6.26.2", sha256="a0f94a72f6188a0a5c855e3362b6b849bf7fd14efc2d824a8d2581f8bb1bd7fa"
    )

    depends_on("r@2.10.0:", type=("build", "run"))
