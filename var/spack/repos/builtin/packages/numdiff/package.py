# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Numdiff(AutotoolsPackage):
    """Numdiff is a little program that can be used to compare putatively
    similar files line by line and field by field, ignoring small numeric
    differences or/and different numeric formats."""

    homepage = "https://www.nongnu.org/numdiff"
    url = "https://nongnu.askapache.com/numdiff/numdiff-5.8.1.tar.gz"

    license("GPL-3.0-only")

    version("5.9.0", sha256="87284a117944723eebbf077f857a0a114d818f8b5b54d289d59e73581194f5ef")
    version("5.8.1", sha256="99aebaadf63325f5658411c09c6dde60d2990c5f9a24a51a6851cb574a4af503")

    depends_on("c", type="build")  # generated

    variant("nls", default=False, description="Enable Natural Language Support")
    variant("gmp", default=False, description="Use GNU Multiple Precision Arithmetic Library")

    depends_on("gettext", when="+nls")
    depends_on("gmp", when="+gmp")

    def configure_args(self):
        spec = self.spec
        args = []
        if "+nls" in spec:
            args.append("--enable-nls")
        else:
            args.append("--disable-nls")

        if "+gmp" in spec:
            # compile with -O0 as per upstream known issue with optimization
            # and GMP; https://launchpad.net/ubuntu/+source/numdiff/+changelog
            # http://www.nongnu.org/numdiff/#issues
            # keep this variant off by default as one still encounter
            # GNU MP: Cannot allocate memory (size=2305843009206983184)
            args.extend(["--enable-gmp", "CFLAGS=-O0"])
        else:
            args.append("--disable-gmp")

        return args
