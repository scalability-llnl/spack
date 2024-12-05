# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlYamlTiny(PerlPackage):
    """YAML::Tiny - Read/Write YAML files with as little code as possible"""

    homepage = "https://metacpan.org/pod/YAML::Tiny"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/YAML-Tiny-1.73.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.74", sha256="7b38ca9f5d3ce24230a6b8bdc1f47f5b2db348e7f7f9666c26f5955636e33d6c")
    version("1.73", sha256="bc315fa12e8f1e3ee5e2f430d90b708a5dc7e47c867dba8dce3a6b8fbe257744")
