# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class DeprecatedVersions(Package):
    """Package with the most recent version deprecated"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/c-1.0.tar.gz"

    version(
        "1.1.0",
        sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
        deprecated=True,
    )
    version("1.0.0", sha256="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890")
