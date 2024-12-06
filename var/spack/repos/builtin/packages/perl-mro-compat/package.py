# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMroCompat(PerlPackage):
    """Provides several utilities for dealing with method resolution order."""

    homepage = "https://metacpan.org/pod/MRO::Compat"
    url = "http://search.cpan.org/CPAN/authors/id/H/HA/HAARG/MRO-Compat-0.13.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.15", sha256="0d4535f88e43babd84ab604866215fc4d04398bd4db7b21852d4a31b1c15ef61")
    version("0.13", sha256="8a2c3b6ccc19328d5579d02a7d91285e2afd85d801f49d423a8eb16f323da4f8")
