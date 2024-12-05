# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IkeScan(AutotoolsPackage):
    """Discover and fingerprint IKE hosts (IPsec VPN Servers)."""

    homepage = "https://github.com/royhills/ike-scan"
    url = "https://github.com/royhills/ike-scan/releases/download/1.9/ike-scan-1.9.tar.gz"

    license("GPL-2.0-or-later")

    version("1.9", sha256="05d15c7172034935d1e46b01dacf1101a293ae0d06c0e14025a4507656f1a7b6")

    depends_on("c", type="build")  # generated
