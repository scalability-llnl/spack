# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlInlineC(PerlPackage):
    """C Language Support for Inline"""

    homepage = "https://metacpan.org/pod/Inline::C"
    url = "http://search.cpan.org/CPAN/authors/id/T/TI/TINITA/Inline-C-0.78.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.81", sha256="f185258d9050d7f79b4f00f12625cc469c2f700ff62d3e831cb18d80d2c87aac")
    version("0.78", sha256="9a7804d85c01a386073d2176582b0262b6374c5c0341049da3ef84c6f53efbc7")

    depends_on("perl-yaml-libyaml", type=("build", "run"))
    depends_on("perl-parse-recdescent", type=("build", "run"))
    depends_on("perl-inline", type=("build", "run"))
    depends_on("perl-pegex", type=("build", "run"))
    depends_on("perl-file-copy-recursive", type=("build", "run"))
