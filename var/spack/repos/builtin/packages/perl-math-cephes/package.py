# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMathCephes(PerlPackage):
    """This module provides an interface to over 150 functions of the
    cephes math library of Stephen Moshier."""

    homepage = "https://metacpan.org/pod/Math::Cephes"
    url = "http://search.cpan.org/CPAN/authors/id/S/SH/SHLOMIF/Math-Cephes-0.5305.tar.gz"

    license("Artistic-1.0")

    version("0.5305", sha256="561a800a4822e748d2befc366baa4b21e879a40cc00c22293c7b8736caeb83a1")

    depends_on("c", type="build")  # generated
