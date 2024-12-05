# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTryTiny(PerlPackage):
    """Minimal try/catch with proper preservation of $@"""

    homepage = "https://metacpan.org/pod/Try::Tiny"
    url = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Try-Tiny-0.28.tar.gz"

    license("MIT")

    version("0.31", sha256="3300d31d8a4075b26d8f46ce864a1d913e0e8467ceeba6655d5d2b2e206c11be")
    version("0.28", sha256="f1d166be8aa19942c4504c9111dade7aacb981bc5b3a2a5c5f6019646db8c146")
