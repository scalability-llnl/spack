# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStringApprox(PerlPackage):
    """Perl extension for approximate matching (fuzzy matching)"""

    homepage = "https://metacpan.org/pod/String::Approx"
    url = "https://cpan.metacpan.org/authors/id/J/JH/JHI/String-Approx-3.28.tar.gz"

    maintainers("EbiArnie")

    version("3.28", sha256="43201e762d8699cb0ac2c0764a5454bdc2306c0771014d6c8fba821480631342")

    depends_on("c", type="build")  # generated
