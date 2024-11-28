# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPpi(PerlPackage):
    """Parse, Analyze and Manipulate Perl (without perl)"""

    homepage = "https://metacpan.org/pod/PPI"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MITHALDU/PPI-1.277.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.277", sha256="87c79f83b6876e206051965d5019d2507c551f819a86750080ec7ec43b2e0af8")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-class-inspector@1.22:", type=("build", "test"))
    depends_on("perl-clone@0.30:", type=("build", "run", "test"))
    depends_on("perl-params-util@1.00:", type=("build", "run", "test"))
    depends_on("perl-task-weaken", type=("build", "run", "test"))
    depends_on("perl-test-nowarnings", type=("build", "test"))
    depends_on("perl-test-object@0.07:", type=("build", "test"))
    depends_on("perl-test-subcalls@1.07:", type=("build", "test"))
