# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSetIntspan(PerlPackage):
    """Set::IntSpan - Manages sets of integers"""

    homepage = "https://metacpan.org/pod/Set::IntSpan"
    url = "https://cpan.metacpan.org/authors/id/S/SW/SWMCD/Set-IntSpan-1.19.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.19", sha256="11b7549b13ec5d87cc695dd4c777cd02983dd5fe9866012877fb530f48b3dfd0")
