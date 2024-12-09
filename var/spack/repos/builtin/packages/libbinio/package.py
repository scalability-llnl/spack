# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libbinio(AutotoolsPackage):
    """Platform-independent way to access binary data streams in C++."""

    homepage = "https://github.com/adplug/libbinio"
    url = "https://github.com/adplug/libbinio/releases/download/libbinio-1.5/libbinio-1.5.tar.bz2"

    license("LGPL-2.1-or-later")

    version("1.5", sha256="398b2468e7838d2274d1f62dbc112e7e043433812f7ae63ef29f5cb31dc6defd")
    version("1.4", sha256="4a32d3154517510a3fe4f2dc95e378dcc818a4a921fc0cb992bdc0d416a77e75")

    depends_on("cxx", type="build")  # generated
