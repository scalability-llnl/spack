# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPodParser(PerlPackage):
    """Modules for parsing/translating POD format documents"""

    homepage = "https://metacpan.org/pod/Pod::Parser"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MAREKR/Pod-Parser-1.67.tar.gz"

    maintainers("EbiArnie")

    version("1.67", sha256="5deccbf55d750ce65588cd211c1a03fa1ef3aaa15d1ac2b8d85383a42c1427ea")
