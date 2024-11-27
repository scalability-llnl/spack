# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Trident(Package):
    """Trident is a fully supported open source project maintained by
    NetApp. It has been designed from the ground up to help you meet
    the sophisticated persistence demands of your containerized
    applications."""

    homepage = "https://netapp-trident.readthedocs.io"
    url = "https://github.com/NetApp/trident/archive/v20.01.1.tar.gz"

    license("Apache-2.0")

    version("24.02.0", sha256="a0e73a935079114e8a7010766e8a229084638c3c58a7ab6688c51b2d8fd1efa0")
    version("23.01.1", sha256="d0aedf2446e09b15abe9b0f052f42145c6acf23014a6e009e22cff5a2ad6c77d")
    version("20.01.1", sha256="02ba92e569916b98fb1b563c5ef03a94fd7981c3ac1ecb47e69ebb45471dc976")
    version("20.01.0", sha256="5de190579acf62f5e9945dfd45aeb21989272c4972e85cb10256b7ec605c29c7")

    depends_on("go", type="build")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        go = which("go")
        go("build", "-o", prefix.bin)
        with working_dir("cli"):
            go("build", "-o", prefix.bin.tridentctl)
