# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDataPredicate(PerlPackage):
    """Predicate objects for Perl. A predicate object is an object that encapsulates conditions."""

    homepage = "https://metacpan.org/pod/Data::Predicate"
    url = "https://cpan.metacpan.org/authors/id/A/AY/AYATES/data/Data-Predicate-2.1.1.tar.gz"

    maintainers("EbiArnie")

    version("2.1.1", sha256="26d40a54dd3ba3409e847562ef2564a5598bfb3f81c7bd784b608d9bf2222173")

    depends_on("perl-test-exception", type=("build", "test"))
    depends_on("perl-readonly", type=("build", "run", "test"))
