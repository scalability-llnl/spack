# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Constype(AutotoolsPackage, XorgPackage):
    """constype prints on the standard output the Sun code for the type of
    display that the specified device is.

    It was originally written for SunOS, but has been ported to other
    SPARC OS'es and to Solaris on both SPARC & x86."""

    homepage = "https://cgit.freedesktop.org/xorg/app/constype"
    xorg_mirror_path = "app/constype-1.0.4.tar.gz"

    version("1.0.5", sha256="ec7d07204dd5abf8d21d0a89408be17ab316a017838c88b087b127082f02c051")
    version("1.0.4", sha256="ec09aff369cf1d527fd5b8075fb4dd0ecf89d905190cf1a0a0145d5e523f913d")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
