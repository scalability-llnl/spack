# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlConfigGeneral(PerlPackage):
    """Config::General - Generic Config Module"""

    homepage = "https://metacpan.org/pod/Config::General"
    url = "https://cpan.metacpan.org/authors/id/T/TL/TLINDEN/Config-General-2.63.tar.gz"

    license("Artistic-2.0")

    version("2.65", sha256="4d6d5754be3a9f30906836f0cc10e554c8832e14e7a1341efb15b05d706fc58f")
    version("2.63", sha256="0a9bf977b8aabe76343e88095d2296c8a422410fd2a05a1901f2b20e2e1f6fad")

    depends_on("c", type="build")  # generated
