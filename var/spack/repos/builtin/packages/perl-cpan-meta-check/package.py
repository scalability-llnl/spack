# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCpanMetaCheck(PerlPackage):
    """This module verifies if requirements described in a CPAN::Meta object
    are present.."""

    homepage = "https://metacpan.org/pod/CPAN::Meta::Check"
    url = "http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/CPAN-Meta-Check-0.014.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.018", sha256="f619d2df5ea0fd91c8cf83eb54acccb5e43d9e6ec1a3f727b3d0ac15d0cf378a")
    version("0.017", sha256="0454ab93f12780b1d579df15b5f939e09702e954be82028fadd40e8bc9b0f091")
    version("0.014", sha256="28a0572bfc1c0678d9ce7da48cf521097ada230f96eb3d063fcbae1cfe6a351f")

    depends_on("perl-test-deep", type=("build", "run"))
