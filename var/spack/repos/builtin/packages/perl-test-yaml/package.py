# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestYaml(PerlPackage):
    """Testing Module for YAML Implementations"""

    homepage = "https://metacpan.org/pod/Test::YAML"
    url = "https://cpan.metacpan.org/authors/id/T/TI/TINITA/Test-YAML-1.07.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.07", sha256="1f300d034f46298cb92960912cc04bac33fb27f05b8852d8f051e110b9cd995f")

    depends_on("perl-test-base@0.89:", type=("build", "run", "test"))
