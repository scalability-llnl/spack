# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDataStag(PerlPackage):
    """Structured Tags datastructures"""

    homepage = "https://metacpan.org/pod/Data::Stag"
    url = "http://search.cpan.org/CPAN/authors/id/C/CM/CMUNGALL/Data-Stag-0.14.tar.gz"

    version("0.14", sha256="4ab122508d2fb86d171a15f4006e5cf896d5facfa65219c0b243a89906258e59")

    depends_on("c", type="build")  # generated

    depends_on("perl-io-string", type=("build", "run"))
