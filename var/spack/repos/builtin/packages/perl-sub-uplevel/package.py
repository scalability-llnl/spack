# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSubUplevel(PerlPackage):
    """apparently run a function in a higher stack frame"""

    homepage = "https://metacpan.org/pod/Sub::Uplevel"
    url = "http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/Sub-Uplevel-0.2800.tar.gz"

    version("0.2800", sha256="b4f3f63b80f680a421332d8851ddbe5a8e72fcaa74d5d1d98f3c8cc4a3ece293")
