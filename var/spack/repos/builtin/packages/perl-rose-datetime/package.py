# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlRoseDatetime(PerlPackage):
    """DateTime helper functions and objects."""

    homepage = "https://metacpan.org/pod/Rose::DateTime"
    url = "https://cpan.metacpan.org/authors/id/J/JS/JSIRACUSA/Rose-DateTime-0.540.tar.gz"

    maintainers("EbiArnie")

    version("0.540", sha256="1e42802d0944e9669599b7d0dea1e77a0d17a42123f8ca555180db4e7218e34a")

    depends_on("perl-datetime", type=("build", "run", "test"))
    depends_on("perl-rose-object@0.82:", type=("build", "run", "test"))
