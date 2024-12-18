# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpir(Package):
    """Multiple Precision Integers and Rationals."""

    homepage = "https://github.com/wbhart/mpir"
    url = "https://github.com/wbhart/mpir/archive/mpir-2.7.0.tar.gz"
    git = "https://github.com/wbhart/mpir.git"

    license("LGPL-3.0-or-later")

    version("develop", branch="master")
    version("2.7.0", sha256="2d0174aaccff918766215df00420f12929a6c376ab4e558af31f57c55193bcb7")
    version("2.6.0", sha256="dedb336098d41d4e298909586cf351003bcd7aad9317e801f3e4c4838f6d7691")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # This setting allows mpir to act as a drop-in replacement for gmp
    variant("gmp_compat", default=False, description="Compile with GMP library compatibility")

    # Build dependencies
    depends_on("autoconf", type="build")

    # Other dependencies
    depends_on("yasm")

    def install(self, spec, prefix):
        # We definitely don't want to have MPIR build its
        # own version of YASM. This tries to install it
        # to a system directory.
        options = ["--prefix={0}".format(prefix), "--with-system-yasm"]

        if "+gmp_compat" in spec:
            options.extend(["--enable-gmpcompat"])

        configure(*options)
        make()
        if self.run_tests:
            make("check")
        make("install")
