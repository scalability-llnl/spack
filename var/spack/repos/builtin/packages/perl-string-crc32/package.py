# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStringCrc32(PerlPackage):
    """Perl interface for cyclic redundancy check generation"""

    homepage = "https://metacpan.org/pod/String::CRC32"
    url = "https://cpan.metacpan.org/authors/id/L/LE/LEEJO/String-CRC32-2.100.tar.gz"

    maintainers("EbiArnie")

    license("CC0-1.0 OR SSLeay")

    version("2.100", sha256="9706093b2d068b6715d35b4c58f51558e37960083202129fbb00a57e19a74713")

    depends_on("c", type="build")  # generated
