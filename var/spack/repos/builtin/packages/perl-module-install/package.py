# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleInstall(PerlPackage):
    """Module::Install - Standalone, extensible Perl module installer"""

    homepage = "https://metacpan.org/pod/Module::Install"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Module-Install-1.19.tar.gz"

    skip_modules = ["Module::Install"]  # requires prepend "inc::"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.21", sha256="fbf91007f30565f3920e106055fd0d4287981d5e7dad8b35323ce4b733f15a7b")
    version("1.19", sha256="1a53a78ddf3ab9e3c03fc5e354b436319a944cba4281baf0b904fa932a13011b")

    depends_on("perl", type=("build", "run"))
    depends_on("perl-file-remove", type=("build"))
    depends_on("perl-module-build", type=("build"))
    depends_on("perl-module-corelist", type=("build"))
    depends_on("perl-module-scandeps", type=("build"))
    depends_on("perl-yaml-tiny", type=("build"))
