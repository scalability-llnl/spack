# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpeedglm(RPackage):
    """Fitting Linear and Generalized Linear Models to Large Data Sets.

    Fitting linear models and generalized linear models to large data sets by
    updating algorithms."""

    cran = "speedglm"

    license("GPL-2.0-or-later")

    version("0.3-5", sha256="f8663677c10ff324c5639402060ddd2b1a1e917445cb0f8f84e146b85e82bb4b")
    version("0.3-4", sha256="1a12db7dbceaaf5cf4f9a0c03e2a2b9f32e91b697daf2ccfe81bbae9ac3046ce")
    version("0.3-3", sha256="d065d0ee42fb772760fca8d97ad2aa56cd76b1d9ecb4e97478ec362429e16738")
    version("0.3-2", sha256="5fcaf18324dc754152f528a44894944063303f780d33e58569ea7c306bfc45ac")

    depends_on("r-biglm", type=("build", "run"), when="@0.3-5:")
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
