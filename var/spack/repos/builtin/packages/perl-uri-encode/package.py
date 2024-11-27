# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlUriEncode(PerlPackage):
    """This modules provides simple URI (Percent) encoding/decoding"""

    homepage = "https://github.com/mithun/perl-uri-encode"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MITHUN/URI-Encode-v1.1.1.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.1.1", sha256="4bb9ce4e7016c0138cf9c2375508595286efa1c8dc15b45baa4c47281c08243b")

    depends_on("perl-module-build", type="build")
