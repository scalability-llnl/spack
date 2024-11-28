# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTimeClock(PerlPackage):
    """Twenty-four hour clock object with nanosecond precision."""

    homepage = "https://metacpan.org/pod/Time::Clock"
    url = "https://cpan.metacpan.org/authors/id/J/JS/JSIRACUSA/Time-Clock-1.03.tar.gz"

    maintainers("EbiArnie")

    version("1.03", sha256="35e8a8bbfcdb35d86dd4852a9cd32cfb455a9b42e22669186e920c8aca017aef")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
