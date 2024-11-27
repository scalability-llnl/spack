# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlListMoreutils(PerlPackage):
    """Provide the stuff missing in List::Util"""

    homepage = "https://metacpan.org/pod/List::MoreUtils"
    url = "http://search.cpan.org/CPAN/authors/id/R/RE/REHSACK/List-MoreUtils-0.428.tar.gz"

    license("Apache-2.0")

    version("0.430", sha256="63b1f7842cd42d9b538d1e34e0330de5ff1559e4c2737342506418276f646527")
    version("0.428", sha256="713e0945d5f16e62d81d5f3da2b6a7b14a4ce439f6d3a7de74df1fd166476cc2")

    depends_on("perl-exporter-tiny", type=("build", "run"))
    depends_on("perl-list-moreutils-xs", type=("build", "run"))
