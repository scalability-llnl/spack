# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlThrowable(PerlPackage):
    """A role for classes that can be thrown"""

    homepage = "https://metacpan.org/pod/Throwable"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Throwable-1.001.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.001", sha256="d0cb5e9d7d06d70f2cc56eecf857a83a45eaca43850dcdda91d3feb4ddde4c51")

    depends_on("perl-devel-stacktrace@1.32:", type=("run", "test"))
    depends_on("perl-module-runtime@0.002:", type=("run"))
    depends_on("perl-moo@1.000001:", type=("run"))
    depends_on("perl-sub-quote", type=("run"))
