# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fplll(AutotoolsPackage):
    """fplll contains implementations of several lattice algorithms.
    The implementation relies on floating-point orthogonalization,
    and LLL is central to the code, hence the name."""

    homepage = "https://github.com/fplll/fplll"
    url = "https://github.com/fplll/fplll/releases/download/5.4.0/fplll-5.4.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("5.4.4", sha256="0fd9d378f04ff886d8864728baf5d90b8b0b82c1e541e92550644fb54f75691d")
    version("5.4.1", sha256="7bd887957173aa592091772c1c36f6aa606b3b2ace0d14e2c26c7463dcf2deb7")
    version("5.4.0", sha256="fe192a65a56439b098e26e3b7ee224dda7c2c73a58f36ef2cc6f9185ae8c482b")
    version("5.3.3", sha256="5e7c46c30623795feeac19cf607583b7c82b0490ceb91498f0f712789be20ccd")
    version("5.3.2", sha256="4d935d712d11902c60a2a5cb50b696391f4ca4a2de59b0daeca74c29024c21fe")
    version("5.3.1", sha256="bf7e7e667173b5655cb989ec6a55c07af057d9011572f85eb53fbf93f4e2d239")
    version("5.3.0", sha256="67a579842f5dabf9b3968b0c12af1ee808c5bfb7bc611fe4c2bba9ca00af1067")
    version("5.2.1", sha256="e38e3f8f14d5dbf46aab66d6c12f5973d4b12b72832161ed1491e8e925de4816")
    version("5.2.0", sha256="75e17fcaa4fc5fdddbe6eb42aca5f38c4c169a4b52756e74fbe2d1769737ac9c")
    version("5.1.0", sha256="58175c54cc92752576a64361c73e4ea7797fc18fb703b3f22c7570a09075486f")
    version("5.0.3", sha256="d2b11b7dcb26c30ac1aab9ff75aca9b3dd6e0b0b40c382af16017a717dfe05c2")

    depends_on("cxx", type="build")  # generated

    depends_on("gmp")
    depends_on("mpfr")

    def configure_args(self):
        args = ["--with-gmp=" + self.spec["gmp"].prefix, "--with-mpfr=" + self.spec["mpfr"].prefix]
        return args
