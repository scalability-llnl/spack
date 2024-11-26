# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cairomm(AutotoolsPackage):
    """Cairomm is a C++ wrapper for the cairo graphics library."""

    homepage = "https://www.cairographics.org/cairomm/"
    url = "https://cairographics.org/releases/cairomm-1.6.4.tar.gz"

    license("LGPL-2.0-or-later AND MPL-1.1")

    version("1.6.4", sha256="3cb2c898d0ceb94ad2deb722b50a3a6ee46abdda741ecd6e5a40517c85ecea4c")
    version("1.6.2", sha256="068edc1743d92ff1d102141ba7597ba02a47379f9cb97799b0c3310848b56eff")

    depends_on("cxx", type="build")  # generated

    depends_on("cairo")
    depends_on("libsigcpp")
    depends_on("pkgconfig", type="build")
