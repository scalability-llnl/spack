# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleCorelist(PerlPackage):
    """Module::CoreList - what modules shipped with versions of perl"""

    homepage = "https://metacpan.org/pod/Module::CoreList"
    url = "https://cpan.metacpan.org/authors/id/B/BI/BINGOS/Module-CoreList-5.20220820.tar.gz"

    version(
        "5.20240420", sha256="ce3b4548774c6761d91b479cf5b80b10dc74b0c07054dcf3b6252c22639aee8d"
    )
    version(
        "5.20230320", sha256="324a28f755bd10abc26e0e8b6564ae2623276ae99cbb28ee09ced647fa80f87b"
    )
    version(
        "5.20220820", sha256="708effbbf04158b087d34d8acc707f35bdab9dccc61b41d432cb6d995d137f43"
    )
