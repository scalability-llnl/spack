# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStatisticsDescriptive(PerlPackage):
    """Module of basic descriptive statistical functions."""

    homepage = "https://metacpan.org/pod/Statistics::Descriptive"
    url = (
        "http://search.cpan.org/CPAN/authors/id/S/SH/SHLOMIF/Statistics-Descriptive-3.0612.tar.gz"
    )

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("3.0800", sha256="b04edeea26bfed435aa6029956798c281f7f52d4545f3f45b2ad44954e96f939")
    version("3.0612", sha256="772413148e5e00efb32f277c4254aa78b9112490a896208dcd0025813afdbf7a")
