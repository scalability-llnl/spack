# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMemoryProcess(PerlPackage):
    """Memory::Process - Perl class to determine actual memory usage"""

    homepage = "https://metacpan.org/pod/Memory::Process"
    url = "https://cpan.metacpan.org/authors/id/S/SK/SKIM/Memory-Process-0.06.tar.gz"

    license("BSD-2-Clause")

    version("0.06", sha256="35814488ffd29c97621625ea3b3d700afbfa60ed055bd759d4e58d9c8fd44e4e")
