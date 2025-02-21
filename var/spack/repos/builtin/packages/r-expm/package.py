# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RExpm(RPackage):
    """Matrix Exponential, Log, 'etc'.

    Computation of the matrix exponential, logarithm, sqrt, and related
    quantities."""

    cran = "expm"

    license("GPL-2.0-or-later")

    version("1.0-0", sha256="02c536f8f6af55b132210a50b1e9694a3549806bf97c49e0fe03595945aab254")
    version("0.999-7", sha256="28f249b914b8dd33eee16663fc793e57afd0e301e16067bf9f27fa8e591ba0f1")
    version("0.999-6", sha256="2c79912fd2e03fcf89c29f09555880934402fcb2359af8b4579d79b4f955addc")
    version("0.999-4", sha256="58d06427a08c9442462b00a5531e2575800be13ed450c5a1546261251e536096")
    version("0.999-3", sha256="511bac5860cc5b3888bca626cdf23241b6118eabcc82d100935386039e516412")
    version("0.999-2", sha256="38f1e5bfa90f794486789695d0d9e49158c7eb9445dc171dd83dec3d8fa130d6")

    depends_on("r-matrix", type=("build", "run"))
