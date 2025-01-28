# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REcosolver(RPackage):
    """Embedded Conic Solver in R.

    R interface to the Embedded COnic Solver (ECOS), an efficient and robust C
    library for convex problems. Conic and equality constraints can be
    specified in addition to integer and boolean variable constraints for
    mixed-integer problems. This R interface is inspired by the python
    interface and has similar calling conventions."""

    cran = "ECOSolveR"

    version("0.5.5", sha256="2594ed1602b2fe159cc9aff3475e9cba7c1927b496c3daeabc1c0d227943ecc7")
    version("0.5.4", sha256="5d7489e8176c1df3f3f1290732243429280efca4f837916e6b6faa6dc8a8e324")

    depends_on("gmake", type="build")
