# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelSize(PerlPackage):
    """Devel::Size - Perl extension for finding the memory usage of Perl variables"""

    homepage = "https://metacpan.org/pod/Devel::Size"
    url = "https://cpan.metacpan.org/authors/id/N/NW/NWCLARK/Devel-Size-0.83.tar.gz"

    maintainers("snehring")

    version("0.83", sha256="757a67e0aa59ae103ea5ca092cbecc025644ebdc326731688ffab6f8823ef4b3")
    version("0.82_51", sha256="189eb7c528c1fd21ab53675f4f9f75d4651980d72dff3dd01c8b2241bfe7b086")
