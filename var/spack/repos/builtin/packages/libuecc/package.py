# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libuecc(CMakePackage):
    """libuecc is a very small generic-purpose Elliptic Curve Cryptography
    library compatible with Ed25519."""

    homepage = "https://github.com/fars/libuecc"
    url = "https://github.com/fars/libuecc/archive/v7.tar.gz"

    license("BSD-2-Clause")

    version("7", sha256="465a6584c991c13fddf36700328c44fee9a3baff9025fb5f232b34d003d715e0")
    version("6", sha256="ad813abd91462a6b10608e51862a65998649651b22ab5d82f920622cc93befd7")

    depends_on("c", type="build")  # generated
