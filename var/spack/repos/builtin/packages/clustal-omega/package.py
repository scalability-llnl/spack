# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ClustalOmega(AutotoolsPackage):
    """Clustal Omega: the last alignment program you'll ever need."""

    homepage = "http://www.clustal.org/omega/"
    url = "http://www.clustal.org/omega/clustal-omega-1.2.4.tar.gz"

    license("GPL-2.0-or-later")

    version("1.2.4", sha256="8683d2286d663a46412c12a0c789e755e7fd77088fb3bc0342bb71667f05a3ee")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("argtable")
