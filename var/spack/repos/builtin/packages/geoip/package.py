# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Geoip(AutotoolsPackage):
    """Library for country/city/organization to IP address
    or hostname mapping. This package has been deprecated. Use geoip-api-c instead."""

    homepage = "https://www.maxmind.com/app/c"
    url = "https://github.com/maxmind/geoip-api-c/releases/download/v1.6.12/GeoIP-1.6.12.tar.gz"

    license("LGPL-2.1-or-later")

    with default_args(deprecated=True):
        # Note: use geoip-api-c instead
        version(
            "1.6.12", sha256="1dfb748003c5e4b7fd56ba8c4cd786633d5d6f409547584f6910398389636f80"
        )
        version(
            "1.6.11", sha256="b0e5a92200b5ab540d118983f7b7191caf4faf1ae879c44afa3ff2a2abcdb0f5"
        )
        version(
            "1.6.10", sha256="cb44e0d0dbc45efe2e399e695864e58237ce00026fba8a74b31d85888c89c67a"
        )

    depends_on("c", type="build")  # generated
