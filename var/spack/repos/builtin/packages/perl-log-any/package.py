# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLogAny(PerlPackage):
    """Bringing loggers and listeners together"""

    homepage = "https://metacpan.org/pod/Log::Any"
    url = "https://cpan.metacpan.org/authors/id/P/PR/PREACTION/Log-Any-1.717.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.717", sha256="56649da0f3900230c9e3d29252cb0a74806fb2ddebd22805acd7368959a65bca")
