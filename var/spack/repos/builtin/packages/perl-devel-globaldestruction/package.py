# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelGlobaldestruction(PerlPackage):
    """Makes Perl's global destruction less tricky to deal with"""

    homepage = "https://metacpan.org/pod/Devel::GlobalDestruction"
    url = "http://search.cpan.org/CPAN/authors/id/H/HA/HAARG/Devel-GlobalDestruction-0.14.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.14", sha256="34b8a5f29991311468fe6913cadaba75fd5d2b0b3ee3bb41fe5b53efab9154ab")
