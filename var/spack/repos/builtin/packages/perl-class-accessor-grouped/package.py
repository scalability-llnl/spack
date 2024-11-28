# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassAccessorGrouped(PerlPackage):
    """Lets you build groups of accessors"""

    homepage = "https://metacpan.org/pod/Class::Accessor::Grouped"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Class-Accessor-Grouped-0.10014.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.10014", sha256="35d5b03efc09f67f3a3155c9624126c3e162c8e3ca98ff826db358533a44c4bb")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-module-runtime@0.012:", type=("build", "run", "test"))
    depends_on("perl-test-exception@0.31:", type=("build", "test"))
