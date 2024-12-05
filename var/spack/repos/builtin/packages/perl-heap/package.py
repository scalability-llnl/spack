# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHeap(PerlPackage):
    """Perl extensions for keeping data partially sorted"""

    homepage = "https://metacpan.org/pod/Heap"
    url = "https://cpan.metacpan.org/authors/id/J/JM/JMM/Heap-0.80.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.80", sha256="ccda29f3c93176ad0fdfff4dd6f5e4ac90b370cba4b028386b7343bf64139bde")
