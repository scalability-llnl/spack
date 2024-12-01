# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileChangenotify(PerlPackage):
    """Watch for changes to files, cross-platform style"""

    homepage = "https://metacpan.org/pod/File::ChangeNotify"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/File-ChangeNotify-0.31.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("0.31", sha256="192bdb1ce76266c6a694a8e962d039e3adeeb829b6ac1e23f5057f2b506392bd")

    depends_on("perl-module-pluggable", type=("build", "run", "test"))
    depends_on("perl-module-runtime", type=("build", "run", "test"))
    depends_on("perl-moo@1.006:", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean", type=("build", "run", "test"))
    depends_on("perl-test-requires", type=("build", "test"))
    depends_on("perl-test-without-module", type=("build", "test"))
    depends_on("perl-test2-suite", type=("build", "test"))
    depends_on("perl-type-tiny", type=("build", "run", "test"))
