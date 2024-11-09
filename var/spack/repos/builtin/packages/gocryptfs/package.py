# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gocryptfs(GoPackage):
    """Encrypted overlay filesystem written in Go"""

    homepage = "https://nuetzlich.net/gocryptfs/"
    url = (
        "https://github.com/rfjakob/gocryptfs/releases/download/v2.4.0/gocryptfs_v2.4.0_src.tar.gz"
    )

    maintainers("snehring")

    license("MIT", checked_by="snehring")

    version("2.4.0", sha256="26a93456588506f4078f192b70e7816b6a4042a14b748b28a50d2b6c9b10e2ec")

    depends_on("c", type="build")  # generated

    depends_on("openssl")
    depends_on("pkg-config", type="build")
