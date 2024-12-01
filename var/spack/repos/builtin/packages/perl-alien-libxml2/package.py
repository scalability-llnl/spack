# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlAlienLibxml2(PerlPackage):
    """This module provides libxml2 for other modules to use."""

    homepage = "https://metacpan.org/pod/Alien::Libxml2"
    url = "https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Alien-Libxml2-0.10_01.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.19", sha256="f4a674099bbd5747c0c3b75ead841f3b244935d9ef42ba35368024bd611174c9")
    version("0.10_01", sha256="2f45b308b33503292f48bf46a75fe1e653d6b209ba5caf0628d8cc103f8d61ac")

    depends_on("libxml2")
    depends_on("perl-alien-build", type=("build", "run"))
    depends_on("perl-alien-build-plugin-download-gitlab", type=("build", "run"), when="@0.18:")
    depends_on("pkgconfig", type=("build"))
