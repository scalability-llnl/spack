# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpfi(AutotoolsPackage):
    """Library for arbitrary precision interval arithmetic based on MPFR"""

    # Notice: no simple way to deduct URL from version
    homepage = "https://perso.ens-lyon.fr/nathalie.revol/software.html"

    license("LGPL-3.0-only")

    version(
        "1.5.4",
        url="https://gforge.inria.fr/frs/download.php/file/38111/mpfi-1.5.4.tgz",
        sha256="3b3938595d720af17973deaf727cfc0dd41c8b16c20adc103a970f4a43ae3a56",
    )
    version(
        "1.5.3",
        url="https://gforge.inria.fr/frs/download.php/file/37331/mpfi-1.5.3.tar.bz2",
        sha256="2383d457b208c6cd3cf2e66b69c4ce47477b2a0db31fbec0cd4b1ebaa247192f",
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("texinfo", type="build")
    depends_on("gmp", type=("build", "link"))
    depends_on("mpfr", type=("build", "link"))

    def configure_args(self):
        args = ["--with-gmp=" + self.spec["gmp"].prefix, "--with-mpfr=" + self.spec["mpfr"].prefix]
        return args
