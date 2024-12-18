# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Authselect(AutotoolsPackage):
    """Select authentication and indentity profile to use on the system."""

    homepage = "https://github.com/authselect/authselect"
    url = "https://github.com/authselect/authselect/archive/1.2.1.tar.gz"

    license("GPL-3.0-or-later")

    version("1.2.1", sha256="6f58c36d8b405da836dc9d1f44c1a22660c60f9e7ece327138d1b2492cb57749")
    version("1.2", sha256="c354c87a0115612cb51b09b5157f151569e16384cdd69f32b8515209036531b4")
    version("1.1", sha256="39b888575980c1ecac7022dfe5a5452eef59cef850b8544ed5f928e2e8a335dd")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("popt")
