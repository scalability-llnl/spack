# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMinqa(RPackage):
    """Derivative-free optimization algorithms by quadratic approximation.

    Derivative-free optimization by quadratic approximation based on an
    interface to Fortran implementations by M. J. D. Powell."""

    cran = "minqa"

    license("GPL-2.0-only")

    version("1.2.8", sha256="5941e4b9b01978fc6d9fe24e6ca60cca66883fe9fa6ff3cbfa32aa1ac9db5467")
    version("1.2.5", sha256="9b83562390990d04b2c61b63ac9a7c9ecab0d35c460d232596e3c73bdc89f4be")
    version("1.2.4", sha256="cfa193a4a9c55cb08f3faf4ab09c11b70412523767f19894e4eafc6e94cccd0c")

    depends_on("r-rcpp@0.9.10:", type=("build", "run"))
    depends_on("gmake", type="build")
