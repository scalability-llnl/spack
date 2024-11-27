# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libslirp(MesonPackage):
    """General purpose TCP-IP emulator"""

    homepage = "https://gitlab.freedesktop.org/slirp/libslirp"
    url = "https://gitlab.freedesktop.org/slirp/libslirp/-/archive/v4.6.1/libslirp-v4.6.1.tar.gz"
    maintainers("bernhardkaindl")

    license("BSD-3-Clause")

    version("4.7.0", sha256="9398f0ec5a581d4e1cd6856b88ae83927e458d643788c3391a39e61b75db3d3b")
    version("4.6.1", sha256="69ad4df0123742a29cc783b35de34771ed74d085482470df6313b6abeb799b11")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("glib")
