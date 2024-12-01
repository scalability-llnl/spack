# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libao(AutotoolsPackage):
    """A Cross-platform Audio Library."""

    homepage = "https://github.com/xiph/libao/"
    url = "https://github.com/xiph/libao/archive/1.2.2.tar.gz"

    license("GPL-2.0-or-later")

    version("1.2.2", sha256="df8a6d0e238feeccb26a783e778716fb41a801536fe7b6fce068e313c0e2bf4d")
    version("1.2.0", sha256="5ec2d15ee39f218e93a87f5cc8508aaebf5c8b544f42488dcb2b504d97392c99")
    version("1.1.0", sha256="69edc39fa2759133edfcdee0ec47559067a1a8e7cd718db0eb3c82ca4254aa6b")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("perl")
