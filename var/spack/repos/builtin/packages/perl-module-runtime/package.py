# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleRuntime(PerlPackage):
    """Runtime module handling"""

    homepage = "https://metacpan.org/pod/Module::Runtime"
    url = "http://search.cpan.org/CPAN/authors/id/Z/ZE/ZEFRAM/Module-Runtime-0.016.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.016", sha256="68302ec646833547d410be28e09676db75006f4aa58a11f3bdb44ffe99f0f024")

    depends_on("perl-module-build", type="build")
