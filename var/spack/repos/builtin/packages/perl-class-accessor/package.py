# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassAccessor(PerlPackage):
    """Automated accessor generation"""

    homepage = "https://metacpan.org/pod/Class::Accessor"
    url = "https://cpan.metacpan.org/authors/id/K/KA/KASEI/Class-Accessor-0.51.tar.gz"

    maintainers("EbiArnie")

    version("0.51", sha256="bf12a3e5de5a2c6e8a447b364f4f5a050bf74624c56e315022ae7992ff2f411c")
