# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RModelmetrics(RPackage):
    """Rapid Calculation of Model Metrics.

    Collection of metrics for evaluating models written in C++ using 'Rcpp'.
    Popular metrics include area under the curve, log loss, root mean square
    error, etc."""

    cran = "ModelMetrics"

    version("1.2.2.2", sha256="5e06f1926aebca5654e1329c66ef19b04058376b2277ebb16e3bf8c208d73457")
    version("1.2.2", sha256="66d6fc75658287fdbae4d437b51d26781e138b8baa558345fb9e5a2df86a0d95")
    version("1.2.0", sha256="3021ae88733695a35d66e279e8e61861431f14c9916a341f0a562f675cf6ede9")
    version("1.1.0", sha256="487d53fda57da4b29f83a927dda8b1ae6655ab044ee3eec33c38aeb27eed3d85")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.2.2:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-data-table", type=("build", "run"), when="@1.2.0:")
