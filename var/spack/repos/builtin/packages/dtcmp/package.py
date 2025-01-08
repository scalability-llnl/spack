# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dtcmp(AutotoolsPackage):
    """The Datatype Comparison Library provides comparison operations and
    parallel sort algorithms for MPI applications."""

    homepage = "https://github.com/LLNL/dtcmp"
    url = "https://github.com/LLNL/dtcmp/releases/download/v1.0.3/dtcmp-1.0.3.tar.gz"
    git = "https://github.com/LLNL/dtcmp.git"

    maintainers("gonsie", "camstan", "adammoody")

    version("main", branch="main")
    version("1.1.5", sha256="959c28999b8d1dd2e8703172db55392e38114fde0cd54dfad04555622c5e5974")
    version("1.1.4", sha256="dd83d8cecd68e13b78b68e88675cc5847cde06742b7740e140b98f4a08127dd3")
    version("1.1.3", sha256="90b32cadd0ff2f4fa7fc916f8dcfdbe6918e3e285e0292a2470772478ca0aab5")
    version("1.1.2", sha256="76e1d1fed89bf6abf003179a7aed93350d5ce6282cb000b02a241ec802ec399d")
    version("1.1.1", sha256="ddf3c57cbb83515e1b7e4111b8a83f832e66376b40eee5d8a5549dd7b8446bc6")
    version("1.1.0", sha256="fd2c4485eee560a029f62c8f227df4acdb1edc9340907f4ae2dbee59f05f057d")
    version("1.0.3", sha256="1327368e2808043ad5f245cd16f0da19543de50eae02a4e22b8a1c2e0eff8f35")

    depends_on("c", type="build")  # generated

    depends_on("mpi")
    depends_on("lwgrp")

    depends_on("lwgrp@main", when="@main")
    depends_on("lwgrp@1.0.3:", when="@1.1.2:")
    depends_on("lwgrp@1.0.5:", when="@1.1.4:")

    variant("shared", default=True, description="Build with shared libraries")
    depends_on("lwgrp+shared", when="+shared")
    depends_on("lwgrp~shared", when="~shared")

    def configure_args(self):
        args = ["--with-lwgrp=%s" % self.spec["lwgrp"].prefix]
        args.extend(self.enable_or_disable("shared"))
        return args
