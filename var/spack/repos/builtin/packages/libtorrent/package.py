# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libtorrent(AutotoolsPackage):
    """LibTorrent is a BitTorrent library written in C++,
    with a focus on high performance and good code."""

    homepage = "https://github.com/rakshasa/libtorrent"
    url = "https://github.com/rakshasa/libtorrent/archive/v0.13.8.tar.gz"

    license("GPL-2.0-or-later")

    version("0.13.8", sha256="0f6c2e7ffd3a1723ab47fdac785ec40f85c0a5b5a42c1d002272205b988be722")

    depends_on("cxx", type="build")  # generated

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
