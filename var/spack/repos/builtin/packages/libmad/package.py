# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmad(AutotoolsPackage):
    """MAD is a high-quality MPEG audio decoder."""

    homepage = "https://www.underbit.com/products/mad/"
    url = "ftp://ftp.mars.org/pub/mpeg/libmad-0.15.1b.tar.gz"
    list_url = "ftp://ftp.mars.org/pub/mpeg/"

    license("GPL-2.0-or-later")

    version("0.15.1b", sha256="bbfac3ed6bfbc2823d3775ebb931087371e142bb0e9bb1bee51a76a6e0078690")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    # Patch orignally from here, adapted to create missing files:
    # https://www.linuxfromscratch.org/blfs/view/svn/multimedia/libmad.html
    patch("libmad-0.15.1b.patch")

    force_autoreconf = True
