# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSparsem(RPackage):
    """Sparse Linear Algebra.

    Some basic linear algebra functionality for sparse matrices is provided:
    including Cholesky decomposition and backsolving as well as standard R
    subsetting and Kronecker products."""

    cran = "SparseM"

    version("1.84-2", sha256="2580fdbb8679e76c92b9f0c5bd9bb503c4cb6a750ef6ae96595441690ce98665")
    version("1.81", sha256="bd838f381ace680fa38508ff70b3d83cb9ffa28ac1ab568509249bca53c34b33")
    version("1.78", sha256="d6b79ec881a10c91cb03dc23e6e783080ded9db4f2cb723755aa0d7d29a8b432")
    version("1.77", sha256="a9329fef14ae4fc646df1f4f6e57efb0211811599d015f7bc04c04285495d45c")
    version("1.76", sha256="c2c8e44376936a5fe6f09a37f3668016e66cbc687519cc952aa346a658a2b69b")
    version("1.74", sha256="4712f0c80e9f3cb204497f146ba60b15e75976cdb7798996a7c51f841a85eeba")
    version("1.7", sha256="df61550b267f8ee9b9d3b17acbadd57a428b43e5e13a6b1c56ed4c38cb523369")

    depends_on("r@2.15:", type=("build", "run"))
