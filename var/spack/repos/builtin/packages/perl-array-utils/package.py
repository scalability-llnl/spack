# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlArrayUtils(PerlPackage):
    """Small utils for array manipulation"""

    homepage = "https://metacpan.org/pod/Array::Utils"
    url = "http://search.cpan.org/CPAN/authors/id/Z/ZM/ZMIJ/Array/Array-Utils-0.5.tar.gz"

    version("0.5", sha256="89dd1b7fcd9b4379492a3a77496e39fe6cd379b773fd03a6b160dd26ede63770")
