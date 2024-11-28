# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestFileSharedir(PerlPackage):
    """Create a Fake ShareDir for your modules for testing."""

    homepage = "https://metacpan.org/pod/Test::File::ShareDir"
    url = "https://cpan.metacpan.org/authors/id/K/KE/KENTNL/Test-File-ShareDir-1.001002.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.001002", sha256="b33647cbb4b2f2fcfbde4f8bb4383d0ac95c2f89c4c5770eb691f1643a337aad")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-class-tiny", type=("build", "run", "test"))
    depends_on("perl-file-copy-recursive", type=("build", "run", "test"))
    depends_on("perl-file-sharedir@1.00:", type=("build", "run", "test"))
    depends_on("perl-path-tiny@0.018:", type=("build", "run", "test"))
    depends_on("perl-scope-guard", type=("build", "run", "test"))
    depends_on("perl-test-fatal", type=("build", "test"))
