# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBsdResource(PerlPackage):
    """BSD process resource limit and priority functions"""

    homepage = "https://metacpan.org/pod/BSD::Resource"
    url = "https://cpan.metacpan.org/authors/id/J/JH/JHI/BSD-Resource-1.2911.tar.gz"

    maintainers("EbiArnie")

    version("1.2911", sha256="9d1cfba063cc18f72427a22451f7908836b7331ac8785dbe07553c5b043a0c3d")
