# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sessreg(AutotoolsPackage, XorgPackage):
    """Sessreg is a simple program for managing utmp/wtmp entries for X
    sessions. It was originally written for use with xdm, but may also be
    used with other display managers such as gdm or kdm."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/sessreg"
    xorg_mirror_path = "app/sessreg-1.1.0.tar.gz"

    license("ICU")

    version("1.1.3", sha256="6e3e917e881132a7a9ccb181ddd83fe08a99668892455d808c911ad38beea215")
    version("1.1.2", sha256="dbfe74c9af90696b2c6800bd58799e937a6a10eb48a49cc22053e3538fbe361a")
    version("1.1.1", sha256="3e38f72ff690eaffc0f5eaff533a236bb5e93d4b91ed4fff60e9a2505347d009")
    version("1.1.0", sha256="e561edb48dfc3b0624554169c15f9dd2c3139e83084cb323b0c712724f2b6043")

    depends_on("c", type="build")

    depends_on("xproto@7.0.25:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    def patch(self):
        kwargs = {"string": True}
        filter_file("$(CPP) $(DEFS)", "$(CPP) -P $(DEFS)", "man/Makefile.in", **kwargs)
