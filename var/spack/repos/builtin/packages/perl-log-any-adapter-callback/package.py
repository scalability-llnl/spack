# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLogAnyAdapterCallback(PerlPackage):
    """Send Log::Any logs to a subroutine"""

    homepage = "https://metacpan.org/pod/Log::Any::Adapter::Callback"
    url = (
        "https://cpan.metacpan.org/authors/id/P/PE/PERLANCAR/Log-Any-Adapter-Callback-0.102.tar.gz"
    )

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    # Note: Author marked package as deprecated
    version("0.102", sha256="7c01883265bdab65344257c1b1d1e69fbe300e7693dddeebb98f9f67310e07cd")

    depends_on("perl-log-any", type=("build", "run", "test"))
