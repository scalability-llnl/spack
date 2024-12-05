# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNetServer(PerlPackage):
    """Extensible Perl internet server"""

    homepage = "https://metacpan.org/pod/Net::Server"
    url = "https://cpan.metacpan.org/authors/id/R/RH/RHANDOM/Net-Server-2.014.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("2.014", sha256="3406b9ca5a662a0075eed47fb78de1316b601c94f62a0ee34a5544db9baa3720")
