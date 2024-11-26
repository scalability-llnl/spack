# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParamsUtil(PerlPackage):
    """Simple, compact and correct param-checking functions"""

    homepage = "https://metacpan.org/pod/Params::Util"
    url = "https://cpan.metacpan.org/authors/id/R/RE/REHSACK/Params-Util-1.102.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.102", sha256="499bb1b482db24fda277a51525596ad092c2bd51dd508fa8fec2e9f849097402")
    version("1.07", sha256="30f1ec3f2cf9ff66ae96f973333f23c5f558915bb6266881eac7423f52d7c76c")

    def url_for_version(self, version):
        if self.spec.satisfies("@1.099:"):
            return (
                f"https://cpan.metacpan.org/authors/id/R/RE/REHSACK/Params-Util-{version}.tar.gz"
            )
        else:
            return (
                f"http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Params-Util-{version}.tar.gz"
            )
