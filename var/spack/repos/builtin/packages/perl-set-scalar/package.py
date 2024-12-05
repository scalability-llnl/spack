# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSetScalar(PerlPackage):
    """Set::Scalar - basic set operations"""

    homepage = "https://metacpan.org/pod/Set::Scalar"
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAVIDO/Set-Scalar-1.29.tar.gz"

    version("1.29", sha256="a3dc1526f3dde72d3c64ea00007b86ce608cdcd93567cf6e6e42dc10fdc4511d")
