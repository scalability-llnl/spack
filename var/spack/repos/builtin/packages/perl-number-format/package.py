# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNumberFormat(PerlPackage):
    """Number::Format - Perl extension for formatting numbers"""

    homepage = "https://metacpan.org/pod/Number::Format"
    url = "https://cpan.metacpan.org/authors/id/W/WR/WRW/Number-Format-1.75.tar.gz"

    version("1.75", sha256="82d659cb16461764fd44d11a9ce9e6a4f5e8767dc1069eb03467c6e55de257f3")
