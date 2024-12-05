# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTextFormat(PerlPackage):
    """Text::Format - Various subroutines to format text"""

    homepage = "https://metacpan.org/pod/Text::Format"
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Text-Format-0.61.tar.gz"

    license("Artistic-1.0")

    version("0.62", sha256="7d429057319e123c590ba0765334f0ade4a5eb9ea8db7c0ec4d3902de5f90404")
    version("0.61", sha256="bb8a3b8ff515c85101baf553a769337f944a05cde81f111ae78aff416bf4ae2b")

    depends_on("perl-module-build", type="build")
