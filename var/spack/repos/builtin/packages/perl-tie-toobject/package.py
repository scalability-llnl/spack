# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTieToobject(PerlPackage):
    """Tie to an existing object."""

    homepage = "https://metacpan.org/pod/Tie::ToObject"
    url = "https://cpan.metacpan.org/authors/id/N/NU/NUFFIN/Tie-ToObject-0.03.tar.gz"

    maintainers("EbiArnie")

    version("0.03", sha256="a31a0d4430fe14f59622f31db7f25b2275dad2ec52f1040beb030d3e83ad3af4")
