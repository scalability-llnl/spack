# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libnfs(CMakePackage):
    """LIBNFS is a client library for accessing NFS shares over a network."""

    homepage = "https://sites.google.com/site/libnfstarballs/"
    url = "https://github.com/sahlberg/libnfs/archive/libnfs-4.0.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("4.0.0", sha256="6ee77e9fe220e2d3e3b1f53cfea04fb319828cc7dbb97dd9df09e46e901d797d")
    version("3.0.0", sha256="445d92c5fc55e4a5b115e358e60486cf8f87ee50e0103d46a02e7fb4618566a5")
    version("2.0.0", sha256="7ea6cd8fa6c461d01091e584d424d28e137d23ff4b65b95d01a3fd0ef95d120e")
    version("1.11.0", sha256="fc2e45df14d8714ccd07dc2bbe919e45a2e36318bae7f045cbbb883a7854640f")
    version("1.10.0", sha256="7f6c62a05c7e0f0749f2b13f178a4ed7aaf17bd09e65a10bb147bfe9807da272")

    depends_on("c", type="build")  # generated
