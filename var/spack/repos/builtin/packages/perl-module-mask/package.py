# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleMask(PerlPackage):
    """Pretend certain modules are not installed"""

    homepage = "https://metacpan.org/pod/Module::Mask"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MATTLAW/Module-Mask-0.06.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.06", sha256="2d73f81ff21c9fa28102791e546ff257164b3025f7832544c8223fb87c1e7e77")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-module-util@1.00:", type=("build", "run", "test"))
