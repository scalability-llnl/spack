# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPackageVariant(PerlPackage):
    """Parameterizable packages"""

    homepage = "https://metacpan.org/pod/Package::Variant"
    url = "https://cpan.metacpan.org/authors/id/M/MS/MSTROUT/Package-Variant-1.003002.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.003002", sha256="b2ed849d2f4cdd66467512daa3f143266d6df810c5fae9175b252c57bc1536dc")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-import-into@1.000000:", type=("build", "run", "test"))
    depends_on("perl-module-runtime@0.013:", type=("build", "run", "test"))
    depends_on("perl-strictures@2.000000:", type=("build", "run", "test"))
    depends_on("perl-test-fatal", type=("build", "test"))
