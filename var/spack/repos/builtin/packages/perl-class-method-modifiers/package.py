# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlClassMethodModifiers(PerlPackage):
    """Class::Method::Modifiers - Provides Moose-like method modifiers"""

    homepage = "https://metacpan.org/pod/Class::Method::Modifiers"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Class-Method-Modifiers-2.13.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.15", sha256="65cd85bfe475d066e9186f7a8cc636070985b30b0ebb1cde8681cf062c2e15fc")
    version("2.13", sha256="ab5807f71018a842de6b7a4826d6c1f24b8d5b09fcce5005a3309cf6ea40fd63")

    depends_on("perl-carp", type=("build", "run"))
    depends_on("perl-exporter-tiny", type=("build", "run"))
