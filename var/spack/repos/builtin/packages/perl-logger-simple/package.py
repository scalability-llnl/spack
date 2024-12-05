# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLoggerSimple(PerlPackage):
    """Implementation of the Simran-Log-Log and Simran-Error-Error modules"""

    homepage = "https://metacpan.org/pod/Logger::Simple"
    url = "https://cpan.metacpan.org/authors/id/T/TS/TSTANLEY/Logger-Simple-2.0.tar.gz"

    version("2.0", sha256="2e63fd3508775b5902132ba1bfb03b42bee468dfaf35dfe42e1909ff6d291b2d")

    depends_on("perl-object-insideout", type=("build", "run"))
