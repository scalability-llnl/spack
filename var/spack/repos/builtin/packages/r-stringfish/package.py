# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStringfish(RPackage):
    """Alt String Implementation.

    Provides an extendable, performant and multithreaded 'alt-string'
    implementation backed by 'C++' vectors and strings."""

    cran = "stringfish"

    maintainers("dorton21")

    license("GPL-3.0-only")

    version("0.16.0", sha256="3608bc83900246297b38df46954bd9aa3b6f463a56eefbe80cfc713eab797993")
    version("0.15.7", sha256="34b1703a8876a40860d35f88a94e069832a7d2bc86189ff07af84ff04fd4b735")
    version("0.15.5", sha256="9df21146a7710e5a9ab4bb53ebc231a580c798b7e541b8d78df53207283f8129")
    version("0.14.2", sha256="9373cfc715cda1527fd20179435977b8e59e19d8c5ef82a31e519f93fb624ced")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r@3.0.2:", type=("build", "run"), when="@0.15.5:")
    depends_on("r-rcpp@0.12.18.3:", type=("build", "run"))
    depends_on("r-rcppparallel", type=("build", "run"))
    depends_on("r-rcppparallel@5.1.4:", type=("build", "run"), when="@0.15.7:")
    depends_on("gmake", type="build")
