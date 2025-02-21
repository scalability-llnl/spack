# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRrblup(RPackage):
    """Ridge Regression and Other Kernels for Genomic Selection.

    Software for genomic prediction with the RR-BLUP mixed model (Endelman
    2011, <doi:10.3835/plantgenome2011.08.0024>). One application is to
    estimate marker effects by ridge regression; alternatively, BLUPs can be
    calculated based on an additive relationship matrix or a Gaussian
    kernel."""

    cran = "rrBLUP"

    version("4.6.3", sha256="cd2a257ecb8252f352fd09189b538db62e4de4a51091cf392c18966c3f0c80cd")
    version("4.6.2", sha256="860f5e3f889593b6737f386743a2679322ec7d3557bea8e25482fd6cb745adff")
    version("4.6.1", sha256="e9230e74cc430a83ac5567071cb1c7f00b35c368f7d79bcc1cfde7225446c4db")
    version("4.6", sha256="28b475a1466fcdc1780caace75cf34155338fda496cebd5799315598a4bc84af")

    depends_on("r@2.14:", type=("build", "run"))
    depends_on("r@4.0:", type=("build", "run"), when="@4.6.2:")
