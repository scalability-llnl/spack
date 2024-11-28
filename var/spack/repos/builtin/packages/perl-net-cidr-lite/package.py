# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNetCidrLite(PerlPackage):
    """Perl extension for merging IPv4 or IPv6 CIDR addresses"""

    homepage = "https://metacpan.org/pod/Net::CIDR::Lite"
    url = "https://cpan.metacpan.org/authors/id/S/ST/STIGTSP/Net-CIDR-Lite-0.22.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.22", sha256="4317d8cb341a617b9e0888da43c09cdffffcb0c9edf7b8c9928d742a563b8517")
