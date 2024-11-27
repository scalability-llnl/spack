# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGetoptTabular(PerlPackage):
    """Getopt::Tabular is a Perl 5 module for table-driven argument parsing,
    vaguely inspired by John Ousterhout's Tk_ParseArgv."""

    homepage = "https://metacpan.org/pod/Getopt::Tabular"
    url = "https://cpan.metacpan.org/authors/id/G/GW/GWARD/Getopt-Tabular-0.3.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.3", sha256="9bdf067633b5913127820f4e8035edc53d08372faace56ba6bfa00c968a25377")
