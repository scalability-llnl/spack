# Copyright Spack Project Developers. See COPYRIGHT file for details.
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

    version("2.5.1", sha256="b2e69d382caef598ffa1071b8d5f6e9df30d38fe2f9e9b0bee0d2e7436654f6d")
    version("2.4.0", sha256="26a93456588506f4078f192b70e7816b6a4042a14b748b28a50d2b6c9b10e2ec")

    depends_on("c", type="build")  # generated

    depends_on("go@1.16:", type="build")
    depends_on("go@1.19:", type="build", when="@2.5:")

    depends_on("openssl")
    depends_on("pkgconfig", type="build")
