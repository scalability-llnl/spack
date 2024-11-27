# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNamespaceAutoclean(PerlPackage):
    """Namespace::Autoclean - Keep imports out of your namespace"""

    homepage = "https://metacpan.org/pod/namespace::autoclean"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/namespace-autoclean-0.29.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.29", sha256="45ebd8e64a54a86f88d8e01ae55212967c8aa8fed57e814085def7608ac65804")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-b-hooks-endofscope@0.12:", type=("build", "run", "test"))
    depends_on("perl-namespace-clean@0.20:", type=("build", "run", "test"))
    depends_on("perl-sub-identify", type=("build", "run", "test"))
    depends_on("perl-test-needs", type=("build", "test"))
