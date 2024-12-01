# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleImplementation(PerlPackage):
    """Loads one of several alternate underlying implementations for a
    module"""

    homepage = "https://metacpan.org/pod/Module::Implementation"
    url = "http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Module-Implementation-0.09.tar.gz"

    license("Artistic-2.0")

    version("0.09", sha256="c15f1a12f0c2130c9efff3c2e1afe5887b08ccd033bd132186d1e7d5087fd66d")

    depends_on("perl-module-runtime", type=("build", "run"))
    depends_on("perl-test-fatal", type=("build", "run"))
    depends_on("perl-test-requires", type=("build", "run"))
    depends_on("perl-try-tiny", type=("build", "run"))
