# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fluxbox(AutotoolsPackage):
    """Fluxbox is a windowmanager for X that was based on the Blackbox 0.61.1 code.

    It is very light on resources and easy to handle but yet full of features
    to make an easy, and extremely fast, desktop experience.
    """

    homepage = "http://fluxbox.org/"
    url = "http://sourceforge.net/projects/fluxbox/files/fluxbox/1.3.7/fluxbox-1.3.7.tar.gz"

    license("MIT")

    version("1.3.7", sha256="c99e2baa06fff1e96342b20415059d12ff1fa2917ade0173c75b2fa570295b9f")

    depends_on("cxx", type="build")  # generated

    # Referenced:https://sourceforge.net/p/fluxbox/bugs/1171/
    patch("fix_zero_comparison.patch")

    depends_on("pkgconfig", type="build")
    depends_on("freetype")
    depends_on("libxrender")
    depends_on("libxext")
    depends_on("expat")
    depends_on("libx11")
