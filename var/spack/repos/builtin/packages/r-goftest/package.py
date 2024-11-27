# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGoftest(RPackage):
    """Classical Goodness-of-Fit Tests for Univariate Distributions.

    Cramer-Von Mises and Anderson-Darling tests of goodness-of-fit for
    continuous univariate distributions, using efficient algorithms."""

    cran = "goftest"

    license("GPL-2.0-or-later")

    version("1.2-3", sha256="3a5f74b6ae7ece5b294781ae57782abe12375d61789c55ff5e92e4aacf347f19")
    version("1.2-2", sha256="e497992666b002b6c6bed73bf05047ad7aa69eb58898da0ad8f1f5b2219e7647")

    depends_on("c", type="build")  # generated

    depends_on("r@3.3:", type=("build", "run"))
