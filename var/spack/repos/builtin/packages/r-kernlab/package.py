# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RKernlab(RPackage):
    """Kernel-Based Machine Learning Lab.

    Kernel-based machine learning methods for classification, regression,
    clustering, novelty detection, quantile regression and dimensionality
    reduction. Among other methods 'kernlab' includes Support Vector Machines,
    Spectral Clustering, Kernel PCA, Gaussian Processes and a QP solver."""

    cran = "kernlab"

    license("GPL-2.0-only")

    version("0.9-33", sha256="70c0787d6d3762c89bb68218fbee19e861fcb5d4c05b787a9692055d95dd3061")
    version("0.9-32", sha256="654ef34e343deb4d2c4c139a44e5397d6e38876088ce1c53c7deb087935d6fdc")
    version("0.9-31", sha256="7359c665c1c5e6780e1ce44b143347c8eec839301c3079d7f19e29159873278a")
    version("0.9-30", sha256="48fc3a839ae57e8ab6ec26a34093ca3306391e7b271bef6e69812e2b4859ee81")
    version("0.9-29", sha256="c3da693a0041dd34f869e7b63a8d8cf7d4bc588ac601bcdddcf7d44f68b3106f")
    version("0.9-27", sha256="f6add50ed4097f04d09411491625f8d46eafc4f003b1c1cff78a6fff8cc31dd4")
    version("0.9-26", sha256="954940478c6fcf60433e50e43cf10d70bcb0a809848ca8b9d683bf371cd56077")
    version("0.9-25", sha256="b9de072754bb03c02c4d6a5ca20f2290fd090de328b55ab334ac0b397ac2ca62")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
