# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xfce4Core(BundlePackage):
    """Core libraries and applications for the Xfce4 desktop environment"""

    homepage = "https://docs.xfce.org/start"

    maintainers("teaguesterling")

    version("4.18")
    version("4.16")

    with when("@4.18"):
        depends_on("libxfce4util@4.18")
        depends_on("xfconf@4.18")
        depends_on("libxfce4ui@4.18")
        depends_on("garcon@4.18.0")
        depends_on("exo@4.18")
        depends_on("thunar@4.18")
        depends_on("xfce4-session@4.18")
        depends_on("xfce4-panel@4.18")
        depends_on("xfce4-settings@4.18")
        depends_on("xfdesktop@4.18")
        depends_on("xfwm4@4.18")
        depends_on("xfce4-appfinder@4.18")
        depends_on("tumbler@4.18")
    with when("@4.16"):
        depends_on("libxfce4util@4.16")
        depends_on("xfconf@4.16")
        depends_on("libxfce4ui@4.16")
        depends_on("garcon@0.8.0")
        depends_on("exo@4.16")
        depends_on("thunar@4.16")
        depends_on("xfce4-session@4.16")
        depends_on("xfce4-panel@4.16")
        depends_on("xfce4-settings@4.16")
        depends_on("xfdesktop@4.16")
        depends_on("xfwm4@4.16")
        depends_on("xfce4-appfinder@4.16")
        depends_on("tumbler@4.16")
