# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleBuildTiny(PerlPackage):
    """Module::Build::Tiny - A tiny replacement for Module::Build"""

    homepage = "https://metacpan.org/pod/Module::Build::Tiny"
    url = "https://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-Tiny-0.039.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.048", sha256="79a73e506fb7badabdf79137a45c6c5027daaf6f9ac3dcfb9d4ffcce92eb36bd")
    version("0.044", sha256="cb053a3049cb717dbf4fd7f3c7ab7c0cb1015b22e2d93f38b1ffc47c078322fd")
    version("0.039", sha256="7d580ff6ace0cbe555bf36b86dc8ea232581530cbeaaea09bccb57b55797f11c")

    depends_on("perl-module-build", type="build")
    depends_on("perl-extutils-config", type=("build", "run"))
    depends_on("perl-extutils-helpers", type=("build", "run"))
    depends_on("perl-extutils-installpaths", type=("build", "run"))
