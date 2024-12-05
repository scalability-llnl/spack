# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlUri(PerlPackage):
    """Uniform Resource Identifiers (absolute and relative)"""

    homepage = "https://metacpan.org/pod/URI"
    url = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/URI-1.72.tar.gz"

    skip_modules = ["URI::urn::isbn"]  # required missing Business::ISBN

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("5.08", sha256="7e2c6fe3b1d5947da334fa558a96e748aaa619213b85bcdce5b5347d4d26c46e")
    version("1.72", sha256="35f14431d4b300de4be1163b0b5332de2d7fbda4f05ff1ed198a8e9330d40a32")
    version("1.71", sha256="9c8eca0d7f39e74bbc14706293e653b699238eeb1a7690cc9c136fb8c2644115")

    depends_on("perl-test-needs", type=("build", "test"))
