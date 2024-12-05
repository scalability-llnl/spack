# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStatisticsBasic(PerlPackage):
    """Statistics::Basic - A collection of very basic statistics modules"""

    homepage = "https://metacpan.org/pod/distribution/Statistics-Basic/lib/Statistics/Basic.pod"
    url = "https://cpan.metacpan.org/authors/id/J/JE/JETTERO/Statistics-Basic-1.6611.tar.gz"

    version("1.6611", sha256="6855ce5615fd3e1af4cfc451a9bf44ff29a3140b4e7130034f1f0af2511a94fb")

    depends_on("perl-number-format", type=("build", "run"))
    depends_on("perl-scalar-list-utils", type=("build", "run"))
