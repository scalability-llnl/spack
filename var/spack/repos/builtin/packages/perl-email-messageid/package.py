# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlEmailMessageid(PerlPackage):
    """Generate world unique message-ids."""

    homepage = "https://metacpan.org/pod/Email::MessageID"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Email-MessageID-1.408.tar.gz"

    maintainers("EbiArnie")

    version("1.408", sha256="1f3d5b4ff0b1c7b39e9ac7c318fb37adcd0bac9556036546494d14f06dc5643c")

    depends_on("perl@5.12.0:", type=("build", "link", "run", "test"))
