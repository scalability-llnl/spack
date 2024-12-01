# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGetoptArgvfile(PerlPackage):
    """Getopt::ArgvFile - interpolates script options from files into @ARGV or another array."""

    homepage = "https://metacpan.org/pod/Getopt::ArgvFile"
    url = "https://cpan.metacpan.org/authors/id/J/JS/JSTENZEL/Getopt-ArgvFile-1.11.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.11", sha256="3709aa513ce6fd71d1a55a02e34d2f090017d5350a9bd447005653c9b0835b22")
