# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlListMoreutilsXs(PerlPackage):
    """List::MoreUtils::XS is a backend for List::MoreUtils. Even if it's
    possible (because of user wishes) to have it practically independent from
    List::MoreUtils, it technically depend on List::MoreUtils. Since it's only
    a backend, the API is not public and can change without any warning."""

    homepage = "https://metacpan.org/pod/List::MoreUtils::XS"
    url      = "https://cpan.metacpan.org/authors/id/R/RE/REHSACK/List-MoreUtils-XS-0.428.tar.gz"

    version('0.428', sha256='9d9fe621429dfe7cf2eb1299c192699ddebf060953e5ebdc1b4e293c6d6dd62d')
